import type { LeaderboardItem } from '../types/radar';

export function Leaderboard({ title, items }: { title: string; items: LeaderboardItem[] }) {
  return (
    <div className="panel">
      <h2>{title}</h2>
      <table>
        <thead>
          <tr><th>Name</th><th>Papers</th><th>Citations</th></tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.name}>
              <td>{item.name}</td>
              <td>{item.paper_count}</td>
              <td>{item.citation_count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
