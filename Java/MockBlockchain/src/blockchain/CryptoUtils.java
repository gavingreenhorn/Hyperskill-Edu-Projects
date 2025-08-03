package blockchain;

import java.nio.charset.StandardCharsets;
import java.security.*;


class CryptoUtils {

    public static KeyPair getAPair() {
        try {
            KeyPairGenerator keygen = KeyPairGenerator.getInstance("RSA");
            keygen.initialize(1024);
            return keygen.generateKeyPair() ;
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }

    public static byte[] sign(String data, PrivateKey key){
        try {
            Signature rsa = Signature.getInstance("SHA1withRSA");
            rsa.initSign(key);
            rsa.update(data.getBytes());
            return rsa.sign();
        } catch (InvalidKeyException | NoSuchAlgorithmException | SignatureException e) {
            throw new RuntimeException(e);
        }
    }

    public static boolean verifySignature(byte[] data, byte[] signature, PublicKey key) {
        try {
            Signature sig = Signature.getInstance("SHA1withRSA");
            sig.initVerify(key);
            sig.update(data);
            return sig.verify(signature);
        } catch (NoSuchAlgorithmException | InvalidKeyException | SignatureException e) {
            throw new RuntimeException(e);
        }
    }

    public static byte[] getRawBytes(String input) {
        MessageDigest digest = null;
        try {
            digest = MessageDigest.getInstance("SHA-256");
            return digest.digest(input.getBytes(StandardCharsets.UTF_8));
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }

    public static String bytesToHex(byte[] bytes) {
        StringBuilder hexString = new StringBuilder();
        for (byte elem: bytes) {
            String hex = Integer.toHexString(0xff & elem);
            if (hex.length() == 1) hexString.append('0');
            hexString.append(hex);
        }
        return hexString.toString();
    }

    public static String applySha256(String input) {
        return bytesToHex(getRawBytes(input));
    }
}