from sklearn.base import BaseEstimator, TransformerMixin


def select_top_categories(df, column, target, n_top_popular=5, n_top_expensive=5):
    counts = df[column].value_counts()
    medians = df.groupby(column)[target].median()

    top_popular = counts.nlargest(n_top_popular).index
    top_expensive = medians.nlargest(n_top_expensive).index

    top_categories = set(top_popular).union(set(top_expensive))
    return top_categories


class CustomNeighbourhoodMedianEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, column="neighbourhood_cleaned", target="price", n_top_popular=7, n_top_expensive=2):
        self.column = column
        self.target = target
        self.n_top_popular = n_top_popular
        self.n_top_expensive = n_top_expensive
        self._medians = None
        self._global_median = None
        self._top_categories = None

    def fit(self, X, y):
        df = X.copy()
        df[self.target] = y

        self._top_categories = select_top_categories(
            df, self.column, self.target, n_top_popular=self.n_top_popular, n_top_expensive=self.n_top_expensive
        )

        df[self.column] = df[self.column].apply(lambda x: x if x in self._top_categories else "Other")

        self._medians = df.groupby(self.column)[self.target].median()
        self._global_median = y.median()
        return self

    def transform(self, X):
        X = X.copy()
        X[self.column] = X[self.column].apply(lambda x: x if x in self._top_categories else "Other")

        X[f"{self.column}_encoded"] = X[self.column].map(self._medians)
        X[f"{self.column}_encoded"] = X[f"{self.column}_encoded"].fillna(self._global_median)

        return X.drop(columns=[self.column])


class PropertyTypeGrouper(BaseEstimator, TransformerMixin):
    def __init__(self, column="property_type", top_n=6):
        self.column = column
        self.top_n = top_n
        self._top_categories = None

    def fit(self, X, y=None):
        counts = X[self.column].value_counts()
        self._top_categories = counts.nlargest(self.top_n).index.tolist()
        return self

    def transform(self, X):
        X = X.copy()
        X[self.column] = X[self.column].apply(lambda x: x if x in self._top_categories else "Other")
        return X
