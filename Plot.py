import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle


def draw(schPlanner, assignments):
    # 定义工件和工序情况

    fig, ax = plt.subplots(figsize=(15, 8))
    colors = ['blue', 'green', 'red']
    fixedColors = ['orange', 'purple', 'gray']

    for assignment in assignments:
        product_type = schPlanner.products[assignments[assignment].productId].productType
        color_index = ord(product_type) - ord('A')  # 计算产品类型在颜色列表中的索引
        fixedColors_index = ord(product_type) - ord('A')
        processStartTime = assignments[assignment].processStartTime
        processDuration = assignments[assignment].processDuration
        prefixStartTime = assignments[assignment].prefixStartTime
        prefixDuration = assignments[assignment].prefixDuration
        resource = assignments[assignment].resourceId
        job = f"{assignments[assignment].productId}"
        process = f"{schPlanner.productSteps[assignments[assignment].productStepId].sequenceNr}"

        # 绘制 processDuration 部分
        ax.broken_barh([(processStartTime, processDuration)], (int(resource[2:]) - 0.4, 0.6), facecolors=colors[color_index],
                       edgecolor='white')

        # 绘制 prefixDuration 部分（如果存在）
        if prefixDuration:
            ax.broken_barh([(prefixStartTime, prefixDuration)], (int(resource[2:]) - 0.4, 0.6),
                           facecolors=fixedColors[fixedColors_index], edgecolor='white')
        # 在绘制 processDuration 部分和 prefixDuration 部分时，将它们组合为一个块
        if prefixDuration:
            ax.broken_barh([(prefixStartTime, prefixDuration)], (int(resource[2:]) - 0.4, 0.6),
                           facecolors=fixedColors[fixedColors_index], edgecolor='black')
            ax.broken_barh([(prefixStartTime + prefixDuration, processDuration)], (int(resource[2:]) - 0.4, 0.6),
                           facecolors=colors[color_index], edgecolor='black')
        else:
            ax.broken_barh([(processStartTime, processDuration)], (int(resource[2:]) - 0.4, 0.6),
                           facecolors=colors[color_index], edgecolor='black')

        # 设置x轴的时间格式
        ax.xaxis_date()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        # 假设其他部分不变，这里只展示对文本对齐方式的调整
        ax.text(prefixStartTime + processDuration / 2, int(resource[2:]), f"({job}-{process})", color='black', ha='center', va='center',
                alpha=0.8)

    ax.set_xlabel('Time')
    ax.set_ylabel('Resources')

    # 设置x轴范围，加上一定的余量用于展示
    max_end_time = max(assignments[assignment].endTime for assignment in assignments)
    min_start_time = min(assignments[assignment].startTime for assignment in assignments)
    ax.set_xlim(min_start_time, max_end_time)

    ax.set_ylim(0.5, max(
        int(assignments[assignment].resourceId[2:])for assignment in assignments) + 0.5)  # 设置y轴范围为最大的resourceId加上一定的余量
    resource_ids = sorted(set(assignments[assignment].resourceId for assignment in assignments),
                          key=lambda x: int(x[1:]))
    ax.set_yticks(range(1, len(resource_ids) + 1))
    ax.set_yticklabels([f'Resource {r}' for r in resource_ids])

    ax.grid(False)
    plt.show()
    print()
