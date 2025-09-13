import matplotlib.pyplot as plt
import pandas as pd

def make_chart():
    df = pd.read_csv('docs/burndown/burndown_sample.csv')
    plt.plot(df['Day'], df['Tasks Remaining'], marker='o')
    plt.title('Burndown Chart')
    plt.xlabel('Day')
    plt.ylabel('Tasks Remaining')
    plt.savefig('docs/burndown/burndown_generated.png')

if __name__ == "__main__":
    make_chart()
