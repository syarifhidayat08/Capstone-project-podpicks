const {
    getAuth,
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signOut,
    sendEmailVerification,
    sendPasswordResetEmail,
  } = require('../config/firebase');
  
  const auth = getAuth();
  
  class FirebaseAuthController {
    async registerUser(req, res) {
      const { email, password } = req.payload;
      console.log("Register User Request:", email, password);
  
      if (!email || !password) {
        return res
          .response({
            email: "Email is required",
            password: "Password is required",
          })
          .code(422);
      }
  
      try {
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        await sendEmailVerification(auth.currentUser);
        return res
          .response({
            message: "Verification email sent! User created successfully!",
          })
          .code(201);
      } catch (error) {
        console.error("Error registering user:", error);
        return res
          .response({
            error: error.message || "An error occurred while registering user",
          })
          .code(500);
      }
    }
  
    async loginUser(req, res) {
      const { email, password } = req.payload;
      console.log("Login User Request:", email, password);
  
      if (!email || !password) {
        return res
          .response({
            email: "Email is required",
            password: "Password is required",
          })
          .code(422);
      }
  
      try {
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        const idToken = userCredential._tokenResponse.idToken;
        if (idToken) {
          res.state("access_token", idToken, {
            httpOnly: true,
            isSecure: process.env.NODE_ENV === "production",
          });
          return res
            .response({ message: "User logged in successfully", userCredential })
            .code(200);
        } else {
          return res.response({ error: "Internal Server Error" }).code(500);
        }
      } catch (error) {
        console.error("Error logging in user:", error);
        return res
          .response({
            error: error.message || "An error occurred while logging in",
          })
          .code(500);
      }
    }
  
    async logoutUser(req, res) {
      console.log("Logout User Request");
      try {
        await signOut(auth);
        res.unstate("access_token");
        return res
          .response({ message: "User logged out successfully" })
          .code(200);
      } catch (error) {
        console.error("Error logging out user:", error);
        return res.response({ error: "Internal Server Error" }).code(500);
      }
    }
  
    async resetPassword(req, res) {
      const { email } = req.payload;
      console.log("Reset Password Request:", email);
  
      if (!email) {
        return res
          .response({
            email: "Email is required",
          })
          .code(422);
      }
  
      try {
        await sendPasswordResetEmail(auth, email);
        return res
          .response({ message: "Password reset email sent successfully!" })
          .code(200);
      } catch (error) {
        console.error("Error resetting password:", error);
        return res.response({ error: "Internal Server Error" }).code(500);
      }
    }
  }
  
  module.exports = new FirebaseAuthController();
  