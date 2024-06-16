require('dotenv').config();
const Hapi = require('@hapi/hapi');
const routes = require('./routes/index'); 
const loadModel = require('./services/loadModel');
const InputError = require('./exceptions/inputError');
const firebaseAdmin = require('firebase-admin'); 
const { admin } = require('./config/firebase'); 
const path = require('path');


const serviceAccountPath = "./path/to/firestore-access/json/hidden";


if (!admin.apps.length) {
    admin.initializeApp({
        credential: admin.credential.cert(require(path.resolve(serviceAccountPath))),
        databaseURL: process.env.FIREBASE_DATABASE_URL,
    });
}

const db = firebaseAdmin.firestore();

const init = async () => {
    try {
        const server = Hapi.server({
            port: process.env.PORT || 3000,
        host: process.env.HOST, 
            routes: {
                cors: {
                    origin: ['*'],
                },
                payload: {
                    parse: true,
                    allow: ['application/json', 'multipart/form-data', 'application/x-www-form-urlencoded'],
                    output: 'data'
                }
            },
        });

        await server.register([
            require('@hapi/inert'),
            require('@hapi/vision'),
            require('@hapi/cookie')
        ]);

        const model = await loadModel();
        server.app.model = model;
        server.app.db = db;

       
        routes.forEach(route => {
            server.route(route);
        });
        console.log('Routes registered:', routes);

        server.ext('onPreResponse', function (request, h) {
            const response = request.response;

            if (response instanceof InputError) {
                const newResponse = h.response({
                    status: 'fail',
                    message: `${response.message} Silakan periksa input Anda.`
                });
                newResponse.code(response.output.statusCode);
                return newResponse;
            }

            if (response.isBoom) {
                const newResponse = h.response({
                    status: 'fail',
                    message: response.output.payload.message
                });
                newResponse.code(response.output.statusCode);
                return newResponse;
            }

            return h.continue;
        });

        await server.start();
        console.log(`Server started at: ${server.info.uri}`);
    } catch (err) {
        console.error('Error starting server:', err);
        process.exit(1);
    }
};

process.on('unhandledRejection', (err) => {
    console.error('Unhandled Rejection:', err);
    process.exit(1);
});

init();
