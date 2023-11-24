function makePlayerCardHtml(player) {
  return `<div class="col col-4">
            <div class='card' style='width: 18rem;'>
              <ul class='list-group list-group-flush'>
                <li class='list-group-item'>${player.name} ${player.team}</li>
                <li class='list-group-item'> Season: 2023</li>
                <li class='list-group-item'> Total Points: ${player.points}</li>
                <li class='list-group-item'> Field Goal %: ${player.field_goal_percent}</li>
                <li class='list-group-item'> Three point %: ${player.three_percent}</li>
                <li class='list-group-item'> Blocks: ${player.blocks}</li>
                <li class='list-group-item'> Assists: ${player.assists}</li>
                <li class='list-group-item'>
                  <form id="add-player-form" data-id="${player.id}" data-player="${player.name}">
                    <div class="form-check">
                      <input class="form-check-input" value="pg" type="radio" name="flexRadioDefault" id="flexRadioDefault1">
                      <label class="form-check-label" for="flexRadioDefault1">
                        Point Guard
                      </label>
                    </div>
                    <div class="form-check">
                      <input class="form-check-input" value="sg" type="radio" name="flexRadioDefault" id="flexRadioDefault2" checked>
                      <label class="form-check-label" for="flexRadioDefault2">
                        Strong Guard
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
                    <button type="submit" class="btn btn-primary" id="add-player-btn" >Add</button>
                  </form>
                </li>
              </ul>
            </div>
          </div>`
}

async function addPlayer(player1, player2) {
  const res = await axios.get('/player/search', {
    params: { player1, player2 },
  });
  
  player1 = res.data.player1;
  player2 = res.data.player2;
  const playerCardHtml1 = makePlayerCardHtml(player1);
  const playerCardHtml2 = makePlayerCardHtml(player2);

  $('#player-cards').append(playerCardHtml1);
  $('#player-cards').append(playerCardHtml2);
  $('#compare-player-form').trigger('reset');
}

$('#compare-player-form').on('submit', async function (event) {
  event.preventDefault()
  $('#player-cards').empty()
  const inputPlayer1 = $('#player1').val()
  const inputPlayer2 = $('#player2').val()

  await addPlayer(inputPlayer1, inputPlayer2)
})

$(document).on('submit', '#add-player-form', function (evt) {
  evt.preventDefault()

  const addPlayerForm = evt.target
  const playerName = addPlayerForm.dataset.player
  let position = ''
  for (let input of addPlayerForm) {
    if (input.checked == true) {
      position = input.value
    }
  }
  const listPositionInput = $(`#${position}`)
  listPositionInput.empty()
  listPositionInput.val(`${playerName}`)
  $('#player-cards').empty()
})
