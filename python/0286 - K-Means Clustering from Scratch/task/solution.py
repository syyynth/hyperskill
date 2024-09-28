import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.datasets import load_wine
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler


def plot_comparison(data: np.ndarray, predicted_clusters: np.ndarray, true_clusters: np.ndarray = None,
                    centers: np.ndarray = None, show: bool = True):
    # Use this function to visualize the results on Stage 6.

    if true_clusters is not None:
        plt.figure(figsize=(20, 10))

        plt.subplot(1, 2, 1)
        sns.scatterplot(x=data[:, 0], y=data[:, 1], hue=predicted_clusters, palette='deep')
        if centers is not None:
            sns.scatterplot(x=centers[:, 0], y=centers[:, 1], marker='X', color='k', s=200)
        plt.title('Predicted clusters')
        plt.xlabel('alcohol')
        plt.ylabel('malic_acid')
        plt.grid()

        plt.subplot(1, 2, 2)
        sns.scatterplot(x=data[:, 0], y=data[:, 1], hue=true_clusters, palette='deep')
        if centers is not None:
            sns.scatterplot(x=centers[:, 0], y=centers[:, 1], marker='X', color='k', s=200)
        plt.title('Ground truth')
        plt.xlabel('alcohol')
        plt.ylabel('malic_acid')
        plt.grid()
    else:
        plt.figure(figsize=(10, 10))
        sns.scatterplot(x=data[:, 0], y=data[:, 1], hue=predicted_clusters, palette='deep')
        if centers is not None:
            sns.scatterplot(x=centers[:, 0], y=centers[:, 1], marker='X', color='k', s=200)
        plt.title('Predicted clusters')
        plt.xlabel('alcohol')
        plt.ylabel('malic_acid')
        plt.grid()

    plt.savefig('Visualization.png', bbox_inches='tight')
    if show:
        plt.show()


class CustomKMeans:
    def __init__(self, k):
        self.k = k
        self.centers = None

    def fit(self, X, eps=1e-6):
        self.centers = X[:self.k]

        while True:
            labels = self.predict(X)
            new_centers = self._new_centers(X, labels)

            shift = np.linalg.norm(self.centers - new_centers)

            if shift < eps:
                break

            self.centers = new_centers

        return self

    def _new_centers(self, X, labels):
        return np.array([X[labels == i].mean(axis=0) for i in range(self.k)])

    def predict(self, X):
        return np.argmin(np.linalg.norm(X[:, np.newaxis] - self.centers, axis=2), axis=1)

    def find_inertia(self, X):
        labels = self.predict(X)
        inertia = np.sum((X - self.centers[labels]) ** 2)
        return inertia.tolist()

    def find_silhouette_score(self, X):
        labels = self.predict(X)
        n_samples = X.shape[0]
        unique_labels = np.unique(labels)
        silhouette_vals = np.zeros(n_samples)

        distances = pairwise_distances(X)

        for i in range(n_samples):
            current_label = labels[i]
            current_cluster = labels == current_label

            # cohesion: a(i) - Intra-cluster distance
            a_i = np.mean(distances[i, current_cluster & (np.arange(n_samples) != i)])

            # separation: b(i) - Minimum inter-cluster distance
            b_i = np.min([np.mean(distances[i, labels == label]) for label in unique_labels if label != current_label])

            # silhouette score for point i
            silhouette_vals[i] = (b_i - a_i) / max(a_i, b_i)

        return np.mean(silhouette_vals).tolist()

    @staticmethod
    def find_inertia_for_range(X, k_range):
        return [CustomKMeans(k).fit(X).find_inertia(X) for k in k_range]

    @staticmethod
    def find_silhouette_score_for_range(X, k_range):
        return [CustomKMeans(k).fit(X).find_silhouette_score(X) for k in k_range]


def stage_4():
    inertia_values = CustomKMeans.find_inertia_for_range(X_full, range(2, 11))
    print(inertia_values)

    plt.figure(figsize=(10, 6))
    plt.plot(range(2, 11), inertia_values, 'bx-')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.title('Elbow Method For Optimal k')
    plt.show()


def stage_5():
    silhouette_scores = CustomKMeans.find_silhouette_score_for_range(X_full, range(2, 11))
    print(silhouette_scores)

    plt.figure(figsize=(10, 6))
    plt.plot(range(2, 11), silhouette_scores, 'bx-')
    plt.xlabel('Number of clusters')
    plt.ylabel('Silhouette Score')
    plt.title('Silhouette Score For Different k')
    plt.show()


def stage_6():
    X_selected = X_full[:, [0, 1]]

    kmeans = CustomKMeans(3)
    kmeans.fit(X_full)
    res = kmeans.predict(X_full)
    print(res.tolist()[:20])

    plot_comparison(X_selected, res, y_full.values)


if __name__ == '__main__':
    data = load_wine(as_frame=True, return_X_y=True)
    X_full, y_full = data

    rnd = np.random.RandomState(42)
    permutations = rnd.permutation(len(X_full))
    X_full = X_full.iloc[permutations]
    y_full = y_full.iloc[permutations]

    X_full = StandardScaler().fit_transform(X_full.values)

    # stage_4()
    # stage_5()
    stage_6()
