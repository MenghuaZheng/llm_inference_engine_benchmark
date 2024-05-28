import plotly
import json
import pathlib
import polars as pl 
import plotly.express as px

llamas = pl.concat([
    pl.from_records(json.load(open('result/2024_05_28_10_54_40_llama_llama.cpp.json'))['results']).drop('raw_ticks').sort('batch').with_columns(type=pl.lit('llama-7b@llama.cpp-0.2.5'))
]).to_pandas()

fig_llama_throughput = px.line(llamas, x='batch', y='token_per_s', color='type', title='Llama Throughput')
fig_llama_throughput.write_image('images/llama2-7b-throughput.png', scale=2, width=1440)
fig_llama_throughput.show()

fig_llama_avg_latency = px.line(llamas, x='batch', y='avg_token_latency', color='type', title='Llama Average none-first Token Latency')
fig_llama_avg_latency.write_image('images/llama2-7b-avglat.png', scale=2,width=1440)
fig_llama_avg_latency.show()


fig_llama_avg_latency = px.line(llamas, x='batch', y='avg_first_token_latency', color='type', title='Llama Average First Token Latency')
fig_llama_avg_latency.write_image('images/llama2-7b-first-token-lat.png', scale=2, width=1440)
fig_llama_avg_latency.show()