import copy

import pandas as pd
import numpy as np
import random


original_df = pd.read_csv('output')
df = original_df.drop(['Unnamed: 0', 'name'], axis=1)

diffs = 6
monsters_by_diff = [list() for _ in range(diffs)]


def divide_df_by_diff():
	for i in range(6):
		monsters_by_diff[i] = \
		df[df['difficulty'] == i].reset_index(drop=True)
		# monsters_by_diff[i] = monsters_by_diff[i].to_dict('records')


def normalize():
	global df
	df[df.columns[1:]] -= df[df.columns[1:]].min()
	df[df.columns[1:]] /= (df[df.columns[1:]].max() - df[df.columns[1:]].min())


def balance():
	global df
	divide_df_by_diff()
	target_size = max([len(monsters_by_diff[i]) for i in range(diffs)])

	columns = df.columns[1:]
	new_df = pd.DataFrame(columns=df.columns)

	for i in range(diffs):
		original_instances = copy.deepcopy(monsters_by_diff[i])

		while len(monsters_by_diff[i]) < target_size:
			synthetic_instance = {'difficulty': i}

			r1, r2 = random.sample(range(len(original_instances)), 2)
			instance1 = original_instances.iloc[r1].to_dict()
			instance2 = original_instances.iloc[r2].to_dict()

			rnd_point = random.random()
			for column in df.columns[1:]:
				values = [instance1[column], instance2[column]]

				value = min(values)
				value += rnd_point * (max(values) - min(values))
				synthetic_instance[column] = np.around(value)

			synthetic_instance = pd.DataFrame([synthetic_instance])
			monsters_by_diff[i] = \
			pd.concat([monsters_by_diff[i], synthetic_instance], ignore_index=True)

		new_df = pd.concat([new_df, monsters_by_diff[i]], ignore_index=True)

	df = new_df


def balance_normalize():
	balance()
	normalize()


def main():
	global df

	n = 3
	method = {
		1: normalize,
		2: balance,
		3: balance_normalize
	}[n]
	method()

	df = df.sample(frac=1).reset_index(drop=True)

	if n == 1:
		df.to_csv('normalized_output')

	if n == 2:
		df.to_csv('balanced_output')

	if n == 3:
		df.to_csv('balanced_normalized_output')


if __name__ == '__main__':
	main()
