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
                        <li class='list-group-item'>
                          <form id="add-player-form" data-id="${res.data.results[0].id}" data-player="${res.data.results[0].player_name}">
                            <div class="form-check">
                              <input class="form-check-input" value="sg" type="radio" name="flexRadioDefault" id="flexRadioDefault1">
                              <label class="form-check-label" for="flexRadioDefault1">
                              Strong Guard
                              </label>
                            </div>
                            <div class="form-check">
                              <input class="form-check-input" value="pg" type="radio" name="flexRadioDefault" id="flexRadioDefault2" checked>
                              <label class="form-check-label" for="flexRadioDefault2">
                              Point Guard
                              </label>
                            </div>
                            <div class="form-check">
                              <input class="form-check-input" value="sf" type="radio" name="flexRadioDefault" id="flexRadioDefault2" checked>
                              <label class="form-check-label" for="flexRadioDefault2">
                              Small Forward
                              </label>
                            </div>
                            <div class="form-check">
                              <input class="form-check-input" value="pf" type="radio" name="flexRadioDefault" id="flexRadioDefault2" checked>
                              <label class="form-check-label" for="flexRadioDefault2">
                              Power Forward
                              </label>
                            </div>
                            <div class="form-check">
                              <input class="form-check-input" value="c" type="radio" name="flexRadioDefault" id="flexRadioDefault2" checked>
                              <label class="form-check-label" for="flexRadioDefault2">
                              Center
                              </label>
                            </div>
                            <button type="submit" class="btn btn-primary" id="add-player-btn" >Primary</button>
                          </form>
                        </li>
                        <pre id="log"></pre>
                    </ul>
                </div>
            </div>`;
}

async function addPlayer(player1, player2) {
    const res1 = await axios.get(`https://nba-stats-db.herokuapp.com/api/playerdata/name/${player1}`);
    const res2 = await axios.get(`https://nba-stats-db.herokuapp.com/api/playerdata/name/${player2}`);
    const playerCardHtml1 = makePlayerCardHtml(res1);
    const playerCardHtml2 = makePlayerCardHtml(res2);

    $("#player-cards").append(playerCardHtml1);
    $("#player-cards").append(playerCardHtml2);
    $("#compare-player-form").trigger("reset");
}

$("#compare-player-form").on('submit', async function (event) {
    event.preventDefault();
    $("#player-cards").empty();
    const inputPlayer1 = $('#player1').val();
    const inputPlayer2 = $('#player2').val();
    
    await addPlayer(inputPlayer1, inputPlayer2);
});

$(document).on("submit", "#add-player-form",  function (evt) {
    evt.preventDefault();

    const addPlayerForm = evt.target;
    const playerName = addPlayerForm.dataset.player;
    let position = '';
    for (let input of addPlayerForm) {
        if (input.checked == true) {
            position = input.value;
        };
    };
    const listPosition = $(`#${position}`);
    listPosition.empty();
    listPosition.text(`${playerName}`);
    $("#player-cards").empty();
});


