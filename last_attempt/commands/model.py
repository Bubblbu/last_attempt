from json import dumps
import os
from .base import Base
from lib.client import Client
from lib.simple_window import SimpleWindow
from lib.seq_classifier import SeqClassifier
from collections import deque
from numpy import var

from sklearn.externals import joblib
#from sklearn.neural_netwoemptyrk import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
#from sklearn.gaussian_process import GaussianProcessClassifier
#from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
import pickle
from random import shuffle
from Queue import Queue

class Model(Base):
	"""Do stuff with training data"""
	def __init__(self, *args, **kwargs):
		super(Model, self).__init__(*args, **kwargs)
		self.classifiers = {
			# 'KN': KNeighborsClassifier(3),
			# '': SVC(kernel="linear", C=0.025),
			'SVC': SVC(gamma=2, C=1),
			# 'GPC': GaussianProcessClassifier(1.0 * RBF(1.0), warm_start=True),
			'DTC': DecisionTreeClassifier(max_depth=5),
			'RFC': RandomForestClassifier(max_depth=5, n_estimators=100),
			# 'MLPC': MLPClassifier(alpha=1),
			'ABC': AdaBoostClassifier(),
			'GNB': GaussianNB(),
			'QDA': QuadraticDiscriminantAnalysis()}
		self.deq = None
		self.q = Queue(1)
		self.prev_pred = 0

	def load(self, filename):
		with open(filename, 'r') as fin:
			return pickle.load(fin)

	def discard_transition_samples(self, data_x, data_y, n=30):
		new_data_x = []
		new_data_y = []
		prev = None
		for row, target in zip(data_x, data_y):
			if target != prev:
				k = n

			prev = target

			if k > 0:
				k -= 1
				continue

			new_data_x.append(row)
			new_data_y.append(target)

		return new_data_x, new_data_y

	def run(self):
		if self.options['run-tests']:
			data = self.load("{}.bin".format(self.env_path + "training/" + self.options['--infile']))
			data = self.discard_transition_samples(data[0], data[1])
			data = list(zip(data[0], data[1]))
			shuffle(data)

			data_x = [r[0][:2] + r[0][-2:] for r in data]
			data_y = [r[1] for r in data]

			for key, c in self.classifiers.items():
				print '============'
				print 'Class.: {}'.format(key)
				c.fit(data_x[:-500], data_y[:-500])
				print 'Score: '+ str(c.score(data_x[-500:], data_y[-500:]))
				print '============\n'

		elif self.options['train']:
			data = self.load("{}.bin".format(self.env_path + "training/" + self.options['--infile']))
			data = self.discard_transition_samples(data[0], data[1])
			data = list(zip(data[0], data[1]))
			shuffle(data)

			data_x = [r[0][:2] + r[0][-2:] for r in data]
			data_y = [r[1] for r in data]

			clf = self.classifiers[self.options['--clf']]
			clf.fit(data_x[:-500], data_y[:-500])
			joblib.dump(clf, "{}_{}.pkl".format(self.env_path + "models/" + self.options['--infile'],
												self.options['--clf']))
			print 'Saved clf with score: '+ str(clf.score(data_x[-500:], data_y[-500:]))

		elif self.options['run']:
			scikit_c = joblib.load("{}.pkl".format(self.env_path + "models/" + self.options['--infile']))
			self.clf = SeqClassifier(scikit_c)
			self.window = SimpleWindow(self.q)
			c = Client()
			c.read_stream(self.config.get('openbci','stream-type'), self.data_reader)

	def data_reader(self, data):
		data = self.encode(data)
		prediction = self.clf.predict(data)
		if prediction != self.prev_pred:
			self.q.put(prediction)
			self.prev_pred = prediction

	def encode(self, data):
		if self.deq == None:
			self.deq = [deque(maxlen=40), deque(maxlen=40)]
		self.deq[0].append(data[0])
		self.deq[1].append(data[1])

		return [data[0], data[1], var(self.deq[0]), var(self.deq[1])]
