import dataset_mnist
from sklearn.cluster import KMeans
x, y, _, _ = dataset_mnist.read(selectedLabels=[0,2,7], randomShift=False)


h_kmeans = KMeans(n_clusters=3, random_state=0).fit(x)

dataset_mnist.show(input=x, labels=h_kmeans.predict(x), withVisOfVectorSpace=True)


