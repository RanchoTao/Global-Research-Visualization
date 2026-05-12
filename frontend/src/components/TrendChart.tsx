import { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import type { TrendPoint } from '../types/radar';

export function TrendChart({ trends }: { trends: TrendPoint[] }) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ref.current) return;
    const chart = echarts.init(ref.current);
    chart.setOption({
      tooltip: { trigger: 'axis' },
      legend: { data: ['Papers', 'Citations'] },
      xAxis: { type: 'category', data: trends.map((point) => point.period) },
      yAxis: [{ type: 'value' }, { type: 'value' }],
      series: [
        { name: 'Papers', type: 'bar', data: trends.map((point) => point.paper_count), itemStyle: { color: '#3b82f6' } },
        { name: 'Citations', type: 'line', yAxisIndex: 1, data: trends.map((point) => point.citation_count), itemStyle: { color: '#f97316' } },
      ],
    });
    const resize = () => chart.resize();
    window.addEventListener('resize', resize);
    return () => {
      window.removeEventListener('resize', resize);
      chart.dispose();
    };
  }, [trends]);

  return <div className="chart" ref={ref} />;
}
