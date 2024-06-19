require('dotenv').config();
const Hapi = require('@hapi/hapi');
const routes = require('./routes/index'); 
const firebaseAdmin = require('firebase-admin'); 
const { admin } = require('./config/firebase'); 
const path = require('path');

const serviceAccountPath = './path/service/account/disembunyikan';

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

        
        server.app.db = db;

        routes.forEach(route => {
            server.route(route);
        });
        console.log('Routes registered:', routes);

        

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
