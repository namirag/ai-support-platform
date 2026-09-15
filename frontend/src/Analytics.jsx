import { useEffect, useState } from "react";
import api from "./api";

function Analytics({ refresh }) {
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    const loadAnalytics = async () => {
      try {
        const response = await api.get("/analytics");
        setAnalytics(response.data);
      } catch (error) {
        console.error("Unable to load analytics.");
      }
    };

    loadAnalytics();
  }, [refresh]);

  if (!analytics) {
    return <p>Loading analytics...</p>;
  }

  return (
    <div className="analytics">
      <h2>Support Analytics</h2>

      <div className="analytics-cards">
        <div className="analytics-card">
          <h3>Total Questions</h3>
          <p>{analytics.total_questions}</p>
        </div>

        <div className="analytics-card">
          <h3>Average Rating</h3>
          <p>{analytics.average_rating} / 5</p>
        </div>
      </div>
    </div>
  );
}

export default Analytics;