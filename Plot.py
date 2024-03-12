import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.patches import Rectangle


def draw(schPlanner, assignments):
    # 定义工件和工序情况

    fig, ax = plt.subplots(figsize=(15, 8))
    colors = ['blue', 'green', 'red']

    for assignment in assignments:
        product_type = schPlanner.products[assignments[assignment].productId].productType
        color_index = ord(product_type) - ord('A')  # 计算产品类型在颜色列表中的索引
        start_time = datetime.strptime(assignments[assignment].startTime, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(assignments[assignment].endTime, "%Y-%m-%d %H:%M:%S")
        resource = assignments[assignment].resourceId
        job = f"{assignments[assignment].productId}"
        process = f"{schPlanner.productSteps[assignments[assignment].productStepId].sequenceNr}"
        duration = (end_time - start_time).total_seconds() / 60  # 将持续时间转换为分钟
        start_minute = start_time.hour * 60 + start_time.minute

        ax.broken_barh([(start_minute, duration)], (resource - 0.4, 0.6), facecolors=colors[color_index],
                       edgecolor='white')

        # 添加黑色边框线
        rect = Rectangle((start_minute, resource - 0.4), duration, 0.6, linewidth=1, edgecolor='black',
                         facecolor='none')
        ax.add_patch(rect)

        # 假设其他部分不变，这里只展示对文本对齐方式的调整
        ax.text(start_minute + duration / 2, resource, f"({job}-{process})", color='black', ha='center', va='center',
                alpha=0.8)

    ax.set_xlabel('Time')
    ax.set_ylabel('Machines')
    # 设置x轴范围，加上一定的余量用于展示
    max_end_time = max(
        datetime.strptime(assignments[assignment].endTime, "%Y-%m-%d %H:%M:%S") for assignment in assignments)
    ax.set_xlim(0, max_end_time.hour * 60 + max_end_time.minute + 30)

    ax.set_ylim(0.5, max(
        assignments[assignment].resourceId for assignment in assignments) + 0.5)  # 设置y轴范围为最大的resourceId加上一定的余量
    ax.set_yticks(sorted(set(assignments[assignment].resourceId for assignment in assignments)))
    ax.set_yticklabels(
        [f'Machine {m}' for m in sorted(set(assignments[assignment].resourceId for assignment in assignments))])
    ax.grid(False)
    plt.show()
