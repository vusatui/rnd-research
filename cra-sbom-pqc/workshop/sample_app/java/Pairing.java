import java.security.*;
import javax.crypto.KeyAgreement;

/** Legacy pairing service (fictional). */
public class Pairing {
    public static void main(String[] a) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("RSA");
        kpg.initialize(3072);
        KeyPairGenerator ec = KeyPairGenerator.getInstance("EC");
        KeyAgreement ka = KeyAgreement.getInstance("ECDH");
        Signature s = Signature.getInstance("SHA256withECDSA");
        MessageDigest md = MessageDigest.getInstance("SHA-256");
    }
}
