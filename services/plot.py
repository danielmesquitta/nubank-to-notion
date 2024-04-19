import matplotlib.pyplot as plt
import os

cwd = os.getcwd()


class PieChartDataItem:
  def __init__(self, label: str, size: float | int) -> None:
    self.label = label
    self.size = size


class PlotManager:
  def __init__(self, colors: list[str]) -> None:
    self.colors = colors

  def pie(
          self,
          file_name: str,
          data: list[PieChartDataItem],
  ) -> str:
    labels: list[str] = []
    sizes: list[float | int] = []

    for item in data:
      if not isinstance(item, PieChartDataItem):
        raise TypeError('data must be a list of PieChartDataItem')
      labels.append(item.label)
      sizes.append(item.size)

    file_path = os.path.join(cwd, 'tmp', f'{file_name}.png')

    # Set the background color of the figure
    plt.figure(facecolor='#191919')

    plt.pie(sizes, labels=labels, colors=self.colors, shadow=True,
            autopct='%1.1f%%', startangle=140, textprops={'color': 'white'})

    plt.gca().set_facecolor('#191919')

    plt.axis('equal')

    plt.savefig(file_path, bbox_inches='tight')

    return file_path
