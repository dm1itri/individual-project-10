// import {getCookie, getCurrentPlayer, putCurrentPLayer, putHistoryMove, getHistoryMove} from "./withServer";

const diceId = [
    'dicePlaying1',
    'dicePlaying2',
    'dicePlaying3',
    'dicePlaying4',
    'dicePlaying5',
    'dicePlaying6'
];
const questionCards = [1, 2, 3, 4, 5, 6, 8, 10, 11, 13, 14, 15, 16, 17, 18, 20, 22, 23]
const questionBiologyCards = [2, 3, 10, 14, 17, 22]
const questionHistoryCards = [1, 5, 11, 15, 18, 23]
//const questionGeographyCards = [4, 6, 8, 13, 16, 20]
//const questionBiologyCards = [3, 4, 11, 15, 18, 23]
//const questionHistoryCards = [2, 6, 12, 16, 19, 24]
const rusNamePlayers = ['желтый', 'зеленый', 'красный', 'синий']
const enNamePlayers = ['yellow', 'green', 'red', 'blue']
let answerCorrect = {}
let currentPlayer
const gameID = parseInt(document.location.pathname.substring(6))
let playersCoords = []
let playersPoints
let thisPlayer = Number(document.cookie.match(/number_move=(.+?)(;|$)/)[1])
let numberHistory

getCurrentPlayers(gameID)
updateDocument(currentPlayer)


function getCurrentPlayer(gameID) {
    let xhr = new XMLHttpRequest()
    let currPlayer
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if  (xhr.status === 200) {
                currPlayer = JSON.parse(xhr.response)
            }
            else {
                console.log(xhr.status)
            }
        }
    }
    xhr.open('GET', `http://127.0.0.1:5000/api/game/${gameID}`, false)
    xhr.send()
    return currPlayer[gameID]['current_player']
}

function putCurrentPLayer(gameID, skipMove, currentPlayer, playerCoords) {
    let data = new FormData()
    data.append('current_player',  currentPlayer)
    data.append('current_position', playerCoords)
    data.append('skipping_move', skipMove)
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if  (xhr.status !== 200) {
                console.log(xhr.status)
            }
        }
    }
    xhr.open('PUT', `http://127.0.0.1:5000/api/game/${gameID}`, false)
    xhr.send(data)
}
function putHistoryMove(gameID, currentPlayer, numberSteps) {
    let data = new FormData()
    data.append('number_move',  currentPlayer)
    data.append('number_steps', numberSteps)
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if  (xhr.status !== 200) {
                console.log(xhr.status)
            }
        }
    }
    xhr.open('PUT', `http://127.0.0.1:5000/api/history_game?game_id=${gameID}`, false)
    xhr.send(data)
}
function getHistoryMove(gameID, numberHistory) {
    let xhr = new XMLHttpRequest()
    let history
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if  (xhr.status === 200) {
                history = JSON.parse(xhr.response)
            }
            else {
                console.log(xhr.status)
            }
        }
    }
    xhr.open('GET', `http://127.0.0.1:5000/api/history_game?game_id=${gameID}&number_history=${numberHistory}`, false)
    xhr.send()
    return history[gameID]
}

function getQuestion(typeQuestion) {
    let xhr = new XMLHttpRequest()
    let question
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if  (xhr.status === 200) {
                question = JSON.parse(xhr.response)
            }
            else {
                console.log(xhr.status)
            }
        }
    }
    xhr.open('GET', `http://127.0.0.1:5000/api/question?type_question=${typeQuestion}`, false)
    xhr.send()
    return question
}

function randomIntFromInterval(min, max) { // min and max included
  return Math.floor(Math.random() * (max - min + 1) + min)
}

function getCurrentPlayers(gameID) {
    let games_args
    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
        games_args = JSON.parse(xhr.response)
        }
    }

    xhr.open('GET', `http://127.0.0.1:5000/api/players/${gameID}`, false)
    xhr.send()
    currentPlayer = games_args['current_player']
    numberHistory = games_args['number_history']
    for (let i = 0; i < games_args['count_players']; i++){
        playersCoords.push(games_args[`${i}_player`]['current_position'])
        document.getElementById(`${i}_Player`).style.display = 'block'
        if (playersCoords[i] !== 0) {rollDice(i, 0, playersCoords[i])}
    }
}


async function dicePlaying() {
    document.getElementById('buttonDicePlaying').style.visibility = 'hidden'
    let delay = 100
    let numberSteps = randomIntFromInterval(0, 5)
    let pastIndex
    let interval
    document.getElementById(diceId[numberSteps]).style.display = 'block'
    interval = setInterval(function() {
        pastIndex = numberSteps
        numberSteps = randomIntFromInterval(0, 5)
        numberSteps = (numberSteps === pastIndex) ? (numberSteps + 1) % 6 : numberSteps
        document.getElementById(diceId[numberSteps]).style.display = 'block'
        document.getElementById(diceId[pastIndex]).style.display = 'none'
        }, delay);

    setTimeout(function () {
        clearInterval(interval)
        }, 2000)

    setTimeout(function () {
        document.getElementById(diceId[numberSteps]).style.display = 'none'
        move(currentPlayer, numberSteps + 1)
        // rollDice(currentPlayer, playersCoords[currentPlayer], currentIndex + 1)
    }, 3000) // 3000
}

function rollDice (numberPlayer, index_0, number_steps) {
    const square_cards = [0, 7, 12, 19]
    let realCoords = index_0
    let move
    if (index_0 >= 19) {
        index_0 -= 19
    } else if (index_0 >= 12) {
        index_0 -= 12
    } else if (index_0 >= 7) {
        index_0 -=7
    }

    for (let i = 1; i <= number_steps; i++) {
        if (0 <= realCoords && realCoords < 7) {
            if (numberPlayer % 2) {
                move =  realCoords !== 6 ? index_0  * 100 + 250 : index_0  * 100 + 350
            } else {
                move =  index_0  * 100 + 200
            }
            document.getElementById(`${numberPlayer}_Player`).style.left = move + 'px'
        } else if (7 <= realCoords && realCoords < 12) {
            if (numberPlayer < 2) {
                move = index_0 * 100 + 200
            } else {
                move = realCoords !== 11 ? index_0 * 100 + 250 : index_0 * 100 + 350
            }
            document.getElementById(`${numberPlayer}_Player`).style.top = move + 'px'
        } else if (12 <= realCoords && realCoords < 19) {
            if (numberPlayer % 2) {
                move =  750 - index_0 * 100
            } else {
                move = realCoords !== 18 ? 700 - index_0 * 100 : 700 - index_0 * 100 - 100
            }
            document.getElementById(`${numberPlayer}_Player`).style.left = move + 'px'
        } else {
            if (numberPlayer < 2) {
                move = realCoords !== 23 ? 500 - index_0 * 100 : 500 - index_0 * 100 - 100
            } else {
                move = 550 - index_0 * 100
            }
            document.getElementById(`${numberPlayer}_Player`).style.top = move + 'px'
        }
        realCoords = realCoords === 23 ? 0 : realCoords + 1
        index_0 = square_cards.indexOf(realCoords) === -1 ? index_0 + 1 : 0
    }
    console.log(realCoords)
    return realCoords
}


function checkSquareCards(numberPlayer) {
    if (playersCoords[numberPlayer] === 12) {
        let countSteps = randomIntFromInterval(1, 23)
        setTimeout(rollDice, 1000, numberPlayer, playersCoords[numberPlayer], countSteps)
        putHistoryMove(gameID, currentPlayer, countSteps)
        playersCoords[numberPlayer] = (countSteps + playersCoords[numberPlayer]) % 24
        numberHistory += 1
    }
    if (playersCoords[numberPlayer] === 19) {
        setTimeout(rollDice, 2000, numberPlayer, playersCoords[numberPlayer], 12)
        // 2000 таймаут поставлен, т.к. если попадет сюда с телепорта, то не будет видно перемещение сюда, а сразу в парк
        putHistoryMove(gameID, currentPlayer, 12)
        playersCoords[numberPlayer] = 7
        numberHistory += 1
    }
    if (playersCoords[numberPlayer] === 7) {
        return 1
    }
    return 0
}


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


function updateDocument(currentPlayer) {
    document.getElementById("numberPlayer").innerText = rusNamePlayers[currentPlayer]
    document.getElementById("numberPlayer").style.color = enNamePlayers[currentPlayer]
    document.getElementById("buttonDicePlaying").style.visibility = currentPlayer === thisPlayer ? 'visible' : 'hidden'
}

function updateQuestion(question) {
    document.getElementById("question_1").innerText = question['question']
    for (let i=2; i < 5; i++) {
        document.getElementById(`btn_answer_${i}`).value = question[`answer_${i}`]
    }
    answerCorrect[numberHistory] = randomIntFromInterval(1, 4)

    if (answerCorrect[numberHistory] !== 1) {
        document.getElementById(`btn_answer_1`).value = question[`answer_${answerCorrect[numberHistory]}`]
    }
    document.getElementById(`btn_answer_${answerCorrect[numberHistory]}`).value = question[`answer_correct`]
    document.getElementById("question").style.visibility = 'visible'
}

function clickAnswer1() {
    choosingAnswer(1, numberHistory)
}
function clickAnswer2() {
    choosingAnswer(2,  numberHistory)
}
function clickAnswer3() {
    choosingAnswer(3,  numberHistory)
}
function clickAnswer4() {
    choosingAnswer(4,  numberHistory)
}
function greenAnswer() {
    document.getElementById(`btn_answer_${answerCorrect[numberHistory]}`).style.background = 'rgba(0,255,0,0.71)'
}
function redAnswer(numberAnswer) {
    document.getElementById(`btn_answer_${numberAnswer}`).style.background = 'rgba(255,0,0,0.89)'
}
async function choosingAnswer(numberChoosingAnswer, numberHistory) {
    greenAnswer()
    if (numberChoosingAnswer !== answerCorrect[numberHistory]) {
        redAnswer(numberChoosingAnswer)
    }
    setTimeout(function () {
        document.getElementById(`btn_answer_${answerCorrect[numberHistory]}`).style.background = 'buttonface'
        document.getElementById(`btn_answer_${numberChoosingAnswer}`).style.backgroundColor = 'buttonface'
        document.getElementById("question").style.visibility = 'hidden'
    }, 3000)
    await endMoveAndAnswer(currentPlayer, playersCoords[currentPlayer] === 7 ? 1 : 0, playersCoords[currentPlayer])

}

async function move(numberPlayer, numberSteps) {
    let question
    putHistoryMove(gameID, numberPlayer, numberSteps)
    playersCoords[numberPlayer] = rollDice(numberPlayer, playersCoords[numberPlayer], numberSteps)
    let skippingMove = checkSquareCards(numberPlayer)
    console.log(playersCoords[numberPlayer])
    if ((skippingMove === 0) && (playersCoords[numberPlayer] in questionCards) ) {
        if (questionBiologyCards.indexOf(playersCoords[numberPlayer]) !== -1){
            question = getQuestion('Биология')
            console.log('Биология')
        } else if (questionHistoryCards.indexOf(playersCoords[numberPlayer]) !== -1) {
            question = getQuestion('История')
            console.log('История')
        } else {
            question = getQuestion('География')
        }
        updateQuestion(question)
    }
    else {
        endMoveAndAnswer(numberPlayer, skippingMove, playersCoords[numberPlayer])
    }
}

async function endMoveAndAnswer(numberPlayer, skipMove, playerCoords) {
    putCurrentPLayer(gameID,  skipMove, numberPlayer, playerCoords)
    numberHistory += 1
    currentPlayer = getCurrentPlayer(gameID)
    updateDocument(currentPlayer)
    await waiting_move()
}

async function waiting_move() {
    let numberMove
    let nextHistory
    let t = true
    while (t) {
        currentPlayer = getCurrentPlayer(gameID)
        nextHistory = getHistoryMove(gameID, numberHistory + 1)
        updateDocument(currentPlayer)
        if (currentPlayer === thisPlayer && nextHistory === null) {
            t = false
        } else if (nextHistory === null) {
            await sleep(2000)
        } else {
            numberMove = nextHistory['number_move']
            playersCoords[numberMove] = rollDice(numberMove, playersCoords[numberMove], nextHistory['number_steps'])
            numberHistory += 1
            await sleep (2000)
        }
    }
}

waiting_move()