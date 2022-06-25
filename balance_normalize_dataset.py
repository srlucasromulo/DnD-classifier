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
	print(df)
	df[df.columns[1:]] -= df[df.columns[1:]].min()
	df[df.columns[1:]] /= (df[df.columns[1:]].max() - df[df.columns[1:]].min())


def balance():
	global df
	divide_df_by_diff()
	target_size = max([len(monsters_by_diff[i]) for i in range(diffs)])

	columns = df.columns[1:]
	new_df = pd.DataFrame(columns=df.columns)

	for i in range(diffs):

		value_counts = {}
		for column in columns:
			values = np.array(monsters_by_diff[i][column].value_counts().index)
			counts = np.array(monsters_by_diff[i][column].value_counts().values)
			counts = counts / sum(counts)

			value_counts[column] = {
				'values': values,
				'counts': counts
			}

		while len(monsters_by_diff[i]) < target_size:
			dict = {'difficulty': i}

			for column in columns:
				r1 = np.random.choice(a=value_counts[column]['values'], p=value_counts[column]['counts'])
				r2 = np.random.choice(a=value_counts[column]['values'], p=value_counts[column]['counts'])
				if r1 > r2:
					r1, r2 = r2, r1

				# value = np.random.choice(a=value_counts[column]['values'], p=value_counts[column]['counts'])
				value = np.random.randint(r1, r2) if r1 != r2 else r1
				dict[column] = value

			dict = pd.DataFrame([dict])
			monsters_by_diff[i] = \
			pd.concat([monsters_by_diff[i], dict], ignore_index=True)

		new_df = pd.concat([new_df, monsters_by_diff[i]], ignore_index=True)

	df = new_df


def balance_normalize():
	balance()
	normalize()


def main():
	n = 3
	method = {
		1: normalize,
		2: balance,
		3: balance_normalize
	}[n]
	method()

	if n == 1:
		df.to_csv('normalized_output')

	if n == 2:
		df.to_csv('balanced_output')

	if n == 3:
		df.to_csv('balanced_normalized_output')


if __name__ == '__main__':
	main()
