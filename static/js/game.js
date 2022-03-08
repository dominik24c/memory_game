const CMD_SHOW = 'SHOW';
const HOST =`http://${window.location.host}`;
const PATH_TO_IMG_DIR = `${HOST}/media/cards/`;

const setImgPathAndName = (cardDiv, name, path) => {
    const imgElement = cardDiv.querySelector('img');
    imgElement.setAttribute('src', path);
    imgElement.setAttribute('alt', name);
}

const unsetImgPathAndName= (cardDiv) => {
    const imgElement = cardDiv.querySelector('img');
    imgElement.removeAttribute('src');
    imgElement.removeAttribute('alt');
}


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
        this.board.unsetUnhiddenCards();
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

    setLastUnhiddenCard(cardName) {
        const index = this.unhidden_cards.length - 1;
        if (index === -1) {
            return null;
        }
        const card = this.unhidden_cards[index];
        card.setCard(cardName)
        return card
    }

    unsetUnhiddenCards() {
        this.unhidden_cards.forEach(card => {
            card.unsetCard()
        })
    }

    getCard(x, y) {
        return this.cards[x][y];
    }

    generateBoard(h, w) {
        for (let i = 0; i < h; i++) {
            const vector = [];
            for (let j = 0; j < w; j++) {
                vector.push(null);
            }
            this.cards.push(vector);
        }
    }

    createBoard(size) {
        const sizes = size.split('x')
        this.generateBoard(sizes[0], sizes[1]);
        for (let i = 0; i < this.cards.length; i++) {
            for (let j = 0; j < this.cards[i].length; j++) {
                this.cards[i][j] = new Card(new Position(i, j));
            }
        }
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
    constructor(position) {
        this.path = '';
        this.name = '';
        this.position = new Position(position['x'], position['y']);
        this.cardDiv = null;
    }

    setCard(cardName) {
        setImgPathAndName(this.cardDiv, cardName, `${PATH_TO_IMG_DIR}${cardName}.png`);
    }

    unsetCard() {
        unsetImgPathAndName(this.cardDiv);
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
    if (message && message['BOARD']) {
        game.board.createBoard(message['BOARD']);
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
    } else if (message && message['CARD']) {
        const cardMsg = message['CARD'].split(' ')
        const cardName = cardMsg[0];
        game.board.setLastUnhiddenCard(cardName);
        console.log(cardName);
    } else if (message === 'OK') {
        console.log(message);
    } else if (message === 'ERROR') {
        console.log(message);
    }
}

game_socket.onclose = (e) => {
    console.error("Game socket was closed!")
    window.location.replace(`${HOST}/game`);
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