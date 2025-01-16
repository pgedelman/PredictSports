import React, { useEffect, useState } from "react";
import axios from "axios";

const App = () => {
    const [games, setGames] = useState([]);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/games")
            .then(response => {
                setGames(response.data);
            })
            .catch(error => {
                console.error("Error fetching data:", error);
            });
    }, []);

    return (
        <div>
            <h1>Sports Insights</h1>
            <ul>
                {games.map(game => (
                    <li key={game.game_id}>
                        {game.date} - Home: {game.home_score} vs Away: {game.away_score}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default App;
