const CMD_SHOW = 'SHOW';

class Game {
    constructor() {
        this.board = new Board();
    }

    disableAllCards() {
        this.board.cards.forEach(cardsRow => {
            cardsRow.forEach(card => {
                card.cardDiv.classList.add('card__disable');
            })
        });
    }

    enableAllCards() {
        this.board.cards.forEach(cardsRow => {
            cardsRow.forEach((card) => {
                card.cardDiv.classList.remove('card__disable');
            })
        });
    }

    addCardToUnhiddenCardsArray(card) {
        this.board.unhidden_cards.push(card);
    }


    resetUnhiddenCardsArray() {
        this.board.unhidden_cards.forEach(card => {
            card.hide();
            card.cardDiv.classList.remove('card__disable');
        });
        this.board.unhidden_cards = [];
    }

    removeHitCards() {
        this.board.unhidden_cards.forEach(card => {
            const cardDiv = card.cardDiv;
            cardDiv.onclick = null;
            cardDiv.classList.add('card__remove');
        });
        this.resetUnhiddenCardsArray();
    }
}

class Board {
    constructor() {
        this.cards = [];
        this.unhidden_cards = [];
    }

    getCard(x, y) {
        return this.cards[x][y];
    }

    generateBoard(cards) {
        const n = Math.floor(Math.sqrt(cards.length));
        for (let i = 0; i < n; i++) {
            const vector = [];
            for (let j = 0; j < n; j++) {
                vector.push(null);
            }
            this.cards.push(vector);
        }
    }

    createBoard(cards) {
        this.generateBoard(cards);

        const pathToImgDir = `http://${window.location.host}/media/cards/`;
        cards.forEach(card => {
            const path = `${pathToImgDir}${card['name']}.png`;
            const position = card['position'];
            this.cards[position['x']][position['y']] = new Card(path, card['name'], card['position']);
        });
        console.log(this.cards);
    }

    render() {
        const gameDiv = document.getElementById('game');
        for (let i = 0; i < this.cards.length; i++) {
            for (let j = 0; j < this.cards[i].length; j++) {
                const card = this.cards[i][j];
                gameDiv.appendChild(card.render());
            }
            const brElement = document.createElement('br');
            gameDiv.append(brElement);
        }
    }
}

class Position {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}

class Card {
    constructor(path, name, position) {
        this.path = path;
        this.name = name;
        this.position = new Position(position['x'], position['y']);
        this.cardDiv = null;
    }

    setClassOfImg(className) {
        const imgEl = this.cardDiv.querySelector('img');
        imgEl.className = className;
    }

    hide() {
        this.setClassOfImg('card__hidden');
    }

    show() {
        this.setClassOfImg('card__visible');
    }

    render() {
        this.cardDiv = document.createElement('div')
        this.cardDiv.className = 'card';
        const imgElement = document.createElement('img');
        imgElement.src = this.path;
        imgElement.alt = this.name;
        imgElement.className = 'card__hidden';
        this.cardDiv.appendChild(imgElement);
        this.cardDiv.addEventListener('click', (e) => cardClickHandler(this.position.x, this.position.y));
        return this.cardDiv;
    }
}


const game = new Game();

const gameRoom = document.getElementById('gameRoom').value;

const game_socket = new WebSocket(
    `ws://${window.location.host}/ws/game/${gameRoom}/`
);

game_socket.onmessage = (e) => {
    const data = JSON.parse(e.data);
    console.log(data.message)
    const message = data.message;
    if (message && message['CARDS']) {
        game.board.createBoard(message['CARDS']);
        game.board.render();
    } else if (message === 'HIT') {
        console.log(message);
        setTimeout(() => {
            game.removeHitCards();
            game.enableAllCards();
        }, 2000);
    } else if (message === 'MISSED') {
        console.log(message);
        setTimeout(() => {
            game.resetUnhiddenCardsArray();
            game.enableAllCards();
        }, 4000);
    } else if (message && message['POINTS']) {
        console.log(message['POINTS'])
    } else if (message === 'OK') {
        console.log(message);
    } else if (message === 'ERROR') {
        console.log(message);
    }
}

game_socket.onclose = (e) => {
    console.error("Game socket was closed!");
}

const cardClickHandler = (x, y) => {
    const card = game.board.getCard(x, y);
    card.cardDiv.classList.add('card__disable');
    card.show();
    game.addCardToUnhiddenCardsArray(card);

    if (game.board.unhidden_cards.length === 2) {
        game.disableAllCards();
    }

    game_socket.send(JSON.stringify({
        message: `${CMD_SHOW} ${x} ${y}`
    }));
}