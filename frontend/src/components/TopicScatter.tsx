import { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import type { TopicPoint } from '../types/radar';

export function TopicScatter({ topics }: { topics: TopicPoint[] }) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ref.current) return;
    const chart = echarts.init(ref.current);
    chart.setOption({
      tooltip: {
        formatter: (params: { data: [number, number, number, string, number | null] }) =>
          `<strong>${params.data[3]}</strong><br/>Topic: ${params.data[4] ?? 'n/a'}<br/>Citations: ${params.data[2]}`,
      },
      xAxis: { type: 'value', name: 'Embedding PC1' },
      yAxis: { type: 'value', name: 'Embedding PC2' },
      visualMap: { min: 0, max: 10, dimension: 4, orient: 'horizontal', left: 'center', bottom: 0 },
      series: [
        {
          name: 'Papers',
          type: 'scatter',
          symbolSize: (data: [number, number, number]) => Math.max(8, Math.min(34, 8 + Math.sqrt(data[2]))),
          data: topics.map((point) => [point.x, point.y, point.citation_count, point.title, point.topic_id]),
        },
      ],
    });
    const resize = () => chart.resize();
    window.addEventListener('resize', resize);
    return () => {
      window.removeEventListener('resize', resize);
      chart.dispose();
    };
  }, [topics]);

  return <div className="chart" ref={ref} />;
}
