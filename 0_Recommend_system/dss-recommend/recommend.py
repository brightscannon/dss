import numpy as np
import pandas as pd
from scipy import spatial

class DssSm:

    def intersect_nonzero(self, vector_1, vector_2):
        idx = np.intersect1d(vector_1.nonzero(), vector_2.nonzero())
        vector_1 = vector_1[idx]
        vector_2 = vector_2[idx]
        return vector_1, vector_2

    def euclidean_similarity(self, vector_1, vector_2):
        vector_1, vector_2 = self.intersect_nonzero(vector_1, vector_2)
        if not(len(vector_1) or len(vector_2)):
            return None
        return np.linalg.norm(vector_1 - vector_2)

    def cosine_similarity(self, vector_1, vector_2):
        vector_1, vector_2 = self.intersect_nonzero(vector_1, vector_2)
        if not(len(vector_1) or len(vector_2)):
            return -1
        return 1 - spatial.distance.cosine(vector_1, vector_2)

class DssEvaluate:

    # preprocessing - filtering prediction able datas
    def __preprocessing(self, sample, pred):
        zero_matrix = np.logical_and(sample != 0, pred != 0)
        counts = np.sum(zero_matrix, axis=1)
        c_sample = sample.copy()
        c_pred = pred.copy()
        c_sample[zero_matrix == False] = 0
        c_pred[zero_matrix == False] = 0
        return c_sample, c_pred, counts

    def mse(self, sample, pred):
        sample, pred, counts = self.__preprocessing(sample, pred)
        return np.average(((sample - pred) ** 2).sum(axis=1) / counts)

    def rmse(self, sample, pred):
        sample, pred, counts = self.__preprocessing(sample, pred)
        return np.average(np.sqrt(((sample - pred) ** 2).sum(axis=1)) / counts)

    def mae(self, sample, pred):
        sample, pred, counts = self.__preprocessing(sample, pred)
        return np.average(np.absolute(sample - pred).sum(axis=1) / counts)

class DssRecommend(DssSm, DssEvaluate):

    def __init__(self, sample_df):
        self.sample_df = sample_df
        self.pred_df = None
        self.evaluate_df = None
        self.rm_df = None
        self.is_pred = False
        self.is_evaluate = False
        self.is_rm = False

    def similarity_matrix(self, similarity="cosin"):

        if similarity == "cosin":
            similarity_func = self.cosine_similarity
        elif similarity == "euclidean":
            similarity_func = self.euclidean_similarity

        matrix = []

        for idx1, row1 in self.sample_df.iterrows():
            row = []
            for idx2, row2 in self.sample_df.iterrows():
                row.append(similarity_func(row1.values, row2.values))
            matrix.append(row)

        sm_df = pd.DataFrame(matrix, columns=self.sample_df.index, index=self.sample_df.index)
        sm_df.fillna(sm_df.max().max(), inplace=True)

        return sm_df

    def __pred_score(self, sm_df, user, closer_count):

        user_vec = self.sample_df.loc[user]

        ms_df = sm_df.drop(user)
        ms_df = ms_df.sort_values(user, ascending=False)
        ms_df = ms_df[:closer_count]
        ms_df = self.sample_df.loc[ms_df.index]

        mean_vec = []
        for idx, column in ms_df.items():
            non_zero_count = len(np.nonzero(column.values)[0])
            mean = 0 if non_zero_count == 0 else sum(column.values) / non_zero_count
            mean_vec.append(mean)

        pred_df = pd.DataFrame(columns=self.sample_df.columns)
        pred_df.loc["user"] = self.sample_df.loc[user]
        pred_df.loc["pred"] = mean_vec

        return pred_df


    def pred_matrix(self, similarity="cosin", closer_count=2):

        sm_df = self.similarity_matrix(similarity)
        users = self.sample_df.index

        pred_vecs_1 = []
        pred_vecs_2 = []

        for user in users:
            pred_df = self.__pred_score(sm_df, user, closer_count)
            pred_vecs_1.append(pred_df.loc["pred"].copy())
            idx = pred_df.loc["user"].nonzero()[0]
            pred_df.loc["pred"][idx] = 0
            pred_vecs_2.append(pred_df.loc["pred"])

        non_zero_df = pd.DataFrame(pred_vecs_1, columns=self.sample_df.columns, index=self.sample_df.index)
        is_zero_df = pd.DataFrame(pred_vecs_2, columns=self.sample_df.columns, index=self.sample_df.index)

        self.evaluate_df = non_zero_df
        self.pred_df = is_zero_df
        self.is_pred = True
        self.is_evaluate = True

        return non_zero_df, is_zero_df

    def recommand_matrix(self):

        def recommand_result(user):
            idx = self.pred_df.loc[user].sort_values(ascending=False) > 0
            return list(idx[idx == True].index)

        recommand_dict = {}
        for user in self.sample_df.index:
            recommand_dict[user] = str(recommand_result(user))[1:-1].replace("'","")

        self.rm_df = pd.DataFrame(recommand_dict, index=["recommend"]).T
        self.is_rm = True

        return self.rm_df

    def recommand_user(self, user):
        return self.rm_df.loc[user].values[0].split(",")

    def auto(self, similarity="cosin", closer_count=2):
        self.pred_matrix(similarity, closer_count)
        self.recommand_matrix()

    def evaluate(self):
        return {
            "mse": self.mse(self.sample_df, self.evaluate_df),
            "rmse": self.rmse(self.sample_df, self.evaluate_df),
            "mae": self.mae(self.sample_df, self.evaluate_df),
        }

    def __repr__(self):
        return "<DssRecommend sample_df:{}, pred_df:{}, evaluate_df:{}, rm_df:{}>".format(
            len(self.sample_df), self.is_pred, self.is_evaluate, self.is_rm
        )
