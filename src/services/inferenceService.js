const tf = require('@tensorflow/tfjs-node');
const InputError = require('../exceptions/inputError');

async function predictPodcastRecommendations(model, userInput) {
    try {
       
        const inputTensor = tf.tensor([userInput]); 
        console.log(inputTensor)
       
        const prediction = model.predict(inputTensor);
        
        const recommendations = await prediction.data();
        console.log(recommendations)
        
        return recommendations.map(rec => ({
            Name: rec.Name,
            Genre: rec.Genre,
            Publisher: rec.Publisher,
            SpotifyURL: rec['Spotify URL'],
            CoverImageURL: rec['Cover Image URL']
        }));
    } catch (error) {
        throw new InputError(`Terjadi kesalahan input: ${error.message}`);
    }
}


module.exports = predictPodcastRecommendations;
