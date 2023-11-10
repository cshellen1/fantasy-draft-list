function makePlayerCardHtml(res) {
    return `<div class="col col-4">
                <div class='card' style='width: 18rem;'>
                    <ul class='list-group list-group-flush'>
                        <li class='list-group-item'>${res.data.results[0].player_name} ${res.data.results[0].team}</li>
                        <li class='list-group-item'> Season: ${res.data.results[0].season}</li>
                        <li class='list-group-item'> Total Points: ${res.data.results[0].PTS}</li>
                        <li class='list-group-item'> Field Goal %: ${res.data.results[0].field_percent}</li>
                        <li class='list-group-item'> Three point %: ${res.data.results[0].three_percent}</li>
                        <li class='list-group-item'> Blocks: ${res.data.results[0].BLK}</li>
                        <li class='list-group-item'> Assists: ${res.data.results[0].AST}</li>
                    </ul>
                </div>
            </div>`;
}

async function addPlayer(player) {
    const res = await axios.get(`https://nba-stats-db.herokuapp.com/api/playerdata/name/${player}`);
    const playerCardHtml = makePlayerCardHtml(res);
    $("#player-cards").append(playerCardHtml);
    $("#add-player-form").trigger("reset");
}

$("#add-player-form").on('submit', async function (evt) {
    evt.preventDefault();
    console.log("clicked button");
    const inputPlayer = $('#player').val();
    console.log(inputPlayer);
    await addPlayer(inputPlayer);
});