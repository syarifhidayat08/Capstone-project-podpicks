const { admin } = require("../config/firebase");

const verifyToken = async (request, h) => {
    const idToken = request.headers.authorization && request.headers.authorization.split(' ')[1];

    if (!idToken) {
        return h.response({ error: 'No token provided' }).code(403).takeover();
    }

    try {
        const decodedToken = await admin.auth().verifyIdToken(idToken); 
        request.auth.credentials = decodedToken;
        return h.continue;
    } catch (error) {
        console.error('Error verifying token:', error);
        return h.response({ error: 'Unauthorized' }).code(403).takeover();
    }
};

module.exports = verifyToken;
