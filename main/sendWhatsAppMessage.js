const express = require('express');
const bodyParser = require('body-parser');
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const socketIo = require('socket.io');
const http = require('http');
const qr = require('qr-image');
const fs = require('fs');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.use(bodyParser.json());

// Exibir o QR Code na página web
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

const client = new Client({
    authStrategy: new LocalAuth()
});

client.on('qr', (qrCode) => {
    const qrSvg = qr.image(qrCode, { type: 'svg' });
    let qrCodeString = '';
    qrSvg.on('data', (chunk) => {
        qrCodeString += chunk;
    });
    qrSvg.on('end', () => {
        io.emit('qr', qrCodeString);
    });
});

client.on('ready', () => {
    console.log('Cliente está pronto!');
});

client.on('disconnected', (reason) => {
    console.log('Cliente foi desconectado:', reason);
    client.initialize();
});

client.initialize();

const sendMessage = (telefone, mensagem, nome, tentativas = 3) => {
    return new Promise((resolve, reject) => {
        client.sendMessage(telefone + '@c.us', mensagem)
            .then(response => {
                console.log(`Mensagem enviada com sucesso para ${nome}!`, response);
                resolve(response);
            })
            .catch(err => {
                console.error(`Erro ao enviar mensagem para ${nome}:`, err);
                if (tentativas > 0) {
                    console.log(`Tentando reenviar mensagem para ${nome} (${tentativas - 1} tentativas restantes)...`);
                    setTimeout(() => {
                        sendMessage(telefone, mensagem, nome, tentativas - 1)
                            .then(resolve)
                            .catch(reject);
                    }, 5000);
                } else {
                    console.error(`Falha ao enviar mensagem para ${nome} após múltiplas tentativas.`);
                    reject(err);
                }
            });
    });
};

app.post('/send-messages', async (req, res) => {
    const contatos = req.body.contatos;
    const promises = contatos.map((contato, index) => {
        let telefone = contato.contato;
        telefone = telefone.replace(/[\s\[\]\+\-']/g, '');
        const mensagem = `oi, quero comprar seu carro`;
        return sendMessage(telefone, mensagem, contato.nome);
    });

    try {
        const results = await Promise.all(promises);
        res.send('Mensagens enviadas com sucesso!');
    } catch (err) {
        res.status(500).send('Erro ao enviar algumas mensagens.');
    }
});

server.listen(3000, () => {
    console.log('Servidor rodando na porta 3000');
});
