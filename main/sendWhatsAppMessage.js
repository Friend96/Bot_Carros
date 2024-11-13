const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');

// Inicializar o cliente
const client = new Client({
    authStrategy: new LocalAuth()
});

// Geração de QR Code para autenticação
client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
    console.log('Escaneie o QR Code acima com seu WhatsApp para autenticar.');
});

// Função para enviar mensagem com tentativas de reenvio
const sendMessage = (client, telefone, mensagem, nome, tentativas = 3) => {
    client.sendMessage(telefone + '@c.us', mensagem)
        .then(response => {
            console.log(`Mensagem enviada com sucesso para ${nome}!`, response);
        })
        .catch(err => {
            console.error(`Erro ao enviar mensagem para ${nome}:`, err);
            if (tentativas > 0) {
                console.log(`Tentando reenviar mensagem para ${nome} (${tentativas - 1} tentativas restantes)...`);
                setTimeout(() => sendMessage(client, telefone, mensagem, nome, tentativas - 1), 5000);
            } else {
                console.error(`Falha ao enviar mensagem para ${nome} após múltiplas tentativas.`);
            }
        });
};

// Quando o cliente estiver autenticado
client.on('ready', () => {
    console.log('Cliente está pronto!');

    // Ler o arquivo fones.json
    fs.readFile('fones.json', 'utf8', (err, data) => {
        if (err) {
            console.error('Erro ao ler o arquivo:', err);
            return;
        }

        const contatos = JSON.parse(data);
        contatos.forEach((contato, index) => {
            let telefone = contato.contato;

            // Limpar o número de telefone
            telefone = telefone.replace(/[\s\[\]\+\-']/g, '');

            const mensagem = `oi, quero comprar seu carro`;

            // Enviar mensagem com atraso para evitar sobrecarga
            setTimeout(() => {
                sendMessage(client, telefone, mensagem, contato.nome);
            }, index * 1000); // 1 segundo de atraso entre as mensagens
        });
    });
});

// Capturar erros de desconexão e reconectar
client.on('disconnected', (reason) => {
    console.log('Cliente foi desconectado:', reason);
    client.initialize();
});

// Iniciar o cliente
client.initialize();
