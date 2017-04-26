import dataset_mnist
from sklearn.decomposition import PCA

x, y, _, _ = dataset_mnist.read(randomShift=False)

#show raw data
dataset_mnist.show(input=x, labels=y, withVisOfVectorSpace=True)

h_pca = PCA(n_components=500).fit(x)
#h_pca = PCA(n.components=k).fit(x) 1 up to 784 - the higher the value, the better the reconstruction
#take a look at eigenvalues given by the PCA decomposition and decide
#how many components k you need to keep in order to preserve good
#amounts of information about the data. To get most significant k
#components, where k is number of components you want to keep

#Principal components (eigenvectors of the covariance matrix) are given
#in h_pca.components_. Since these components have the same number of
#attributes/dimensions as x, you can visualise them as images


#show principle components
dataset_mnist.show(input=h_pca.components_)
#components is a kxM matrix where k is the number of components and M is
#the dimensionality of the original dataset. Here, k=M=784

print(h_pca.explained_variance_)
#the components are column vectors ordered from one that preserves most
#information to the one that preserves the least of information. To see the
#eigenvalues, which give the variance of the data projected onto PCA components

x_pca = h_pca.transform(x)
#a Nxk matrix, where N is the number of points in the dataset and k is the num components

x_recovery = h_pca.inverse_transform(x_pca)

#show reconstructed images.
dataset_mnist.show(x_recovery)
