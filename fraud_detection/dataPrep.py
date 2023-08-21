import pandas as pd


class FraudDetection(object):

    def data_preparation(self, df):
        df_copy = df.copy()
        dates = df["step"].values
        hours = []
        num = 0
        for _ in range(0, 743):
            hours.append(num)
            num += 1
            if num % 24 == 0:
                num = 0

        df_hours = pd.DataFrame({"step": dates})
        df_hours["hours"] = hours[dates[0] - 1]

        dataset_hours = pd.merge(df_copy, df_hours, on=['step'], how='left')

        class_hours = pd.DataFrame({'hours': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
                                   'hour_class': [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})

        df_features = pd.merge(dataset_hours, class_hours,
                               on=["hours"], how='left')

        transf = pd.DataFrame({
            "nameDest": df_features['nameDest'].value_counts().index,
            'quanTransf': df_features['nameDest'].value_counts()
        })
        transf = transf.drop(["nameDest"], axis=1)
        transf.reset_index(inplace=True)
        transf = transf.rename(columns = {'index':'nameDest'})
        

        df_final_features = pd.merge(df_features, transf, on=[
                                     'nameDest'], how='left')
        df_final_features = df_final_features.rename(columns={"quanTransf_y": "quanTransf"})

        df_final_features = df_final_features.drop(
            ['step', 'nameOrig', 'nameDest', 'newbalanceDest', 'hours'], axis=1)

        df_final_features['type'] = df_final_features['type'].map(
            {'PAYMENT': 0.0, 'TRANSFER': 1.0, 'CASH_OUT': 2.0, 'DEBIT': 3.0, 'CASH_IN': 4.0})

        return df_final_features
