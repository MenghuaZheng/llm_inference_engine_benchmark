# import plotly
# import json
# import pathlib
# import polars as pl 
# import plotly.express as px

# llamas = pl.concat([
#     pl.from_records(json.load(open('result/2024_05_28_14_32_02_llama_llama.cpp.json'))['results']).drop('raw_ticks').sort('batch').with_columns(type=pl.lit('llama-7b-f32@llama.cpp')),
#     pl.from_records(json.load(open('result/2024_05_29_14_37_12_llama_vllm.json'))['results']).drop('raw_ticks').sort('batch').with_columns(type=pl.lit('llama-7b-f32@vllm'))
# ]).to_pandas()

# fig_llama_throughput = px.line(llamas, x='batch', y='token_per_s', color='type', title='Llama Throughput')
# fig_llama_throughput.write_image('images/llama2-7b-throughput.png', scale=2, width=1440)
# fig_llama_throughput.show()

# fig_llama_avg_latency = px.line(llamas, x='batch', y='avg_token_latency', color='type', title='Llama Average none-first Token Latency')
# fig_llama_avg_latency.write_image('images/llama2-7b-avglat.png', scale=2,width=1440)
# fig_llama_avg_latency.show()


# fig_llama_avg_latency = px.line(llamas, x='batch', y='avg_first_token_latency', color='type', title='Llama Average First Token Latency')
# fig_llama_avg_latency.write_image('images/llama2-7b-first-token-lat.png', scale=2, width=1440)
# fig_llama_avg_latency.show()

import plotly
import json
import pathlib
import polars as pl 
import plotly.express as px
from plotly.subplots import make_subplots


# 读取数据并合并
llamas = pl.concat([
    pl.from_records(json.load(open('result/2024_05_30_11_10_12_llama_llama.cpp.json'))['results']).drop('raw_ticks').sort('batch').with_columns(type=pl.lit('llama-7b-f16@llama.cpp')),
    pl.from_records(json.load(open('result/2024_05_29_14_37_12_llama_vllm.json'))['results']).drop('raw_ticks').sort('batch').with_columns(type=pl.lit('llama-7b-f16@vllm')),
    pl.from_records(json.load(open('result/2024_05_30_11_35_53_llama_fastllm.json'))['results']).drop('raw_ticks').sort('batch').with_columns(type=pl.lit('llama-7b-f16@fastllm'))
]).to_pandas()

def create_and_save_plot(llamas, y_column, title, file_name, log_base='e'):
    fig = make_subplots(rows=1, cols=2, subplot_titles=('Normal Scale', 'Log Scale'))

    # 正常比例图
    fig_normal = px.line(llamas, x='batch', y=y_column, color='type', title=title)
    for trace in fig_normal.data:
        fig.add_trace(trace, row=1, col=1)

    # 对数比例图
    fig_log = px.line(llamas, x='batch', y=y_column, color='type', title=title + ' (Log Scale)')
    for trace in fig_log.data:
        fig.add_trace(trace.update(yaxis='y2'), row=1, col=2)

    # 更新布局
    fig.update_layout(
        yaxis2=dict(type='log', overlaying='y', side='right')
    )

    fig.update_xaxes(title_text="Batch Size", row=1, col=1)
    fig.update_xaxes(title_text="Batch Size", row=1, col=2)

    fig.update_yaxes(title_text="Value", row=1, col=1)
    fig.update_yaxes(title_text="Value (Log Scale)", row=1, col=2)

    # 设置对数坐标轴基数
    if log_base == 'e':
        fig.update_yaxes(dtick='L1', row=1, col=2)  # 自然对数基数
    elif log_base == '2':
        fig.update_yaxes(dtick='L2', row=1, col=2)  # 以2为底的对数
    else:
        fig.update_yaxes(dtick='L10', row=1, col=2)  # 默认以10为底的对数

    # 保存并显示图片
    fig.write_image(file_name, scale=2, width=1880, height=1080)
    fig.show()

# Llama Throughput
create_and_save_plot(llamas, 'token_per_s', 'Llama Throughput', 'images/llama2-7b-throughput.png', log_base='2')

# Llama Average none-first Token Latency
create_and_save_plot(llamas, 'avg_token_latency', 'Llama Average none-first Token Latency', 'images/llama2-7b-avglat.png', log_base='2')

# Llama Average First Token Latency
create_and_save_plot(llamas, 'avg_first_token_latency', 'Llama Average First Token Latency', 'images/llama2-7b-first-token-lat.png', log_base='2')
