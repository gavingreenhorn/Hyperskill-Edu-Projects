package blockchain;

import java.security.KeyPair;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.time.Instant;
import java.util.List;
import java.util.concurrent.atomic.AtomicLong;
import java.util.stream.IntStream;

public class MockClients {

    List<Wallet> generateMockWallets(int walletCount) {
        return IntStream.range(0, walletCount)
            .mapToObj(x -> (Wallet)new WalletImpl(100))
            .toList();
    }

    class WalletImpl implements Wallet {
        private final PrivateKey privateKey;
        private final PublicKey publicKey;
        private final String address;
        private final AtomicLong amount;

        WalletImpl(long initialAmount) {
            KeyPair kp = CryptoUtils.getAPair();
            privateKey = kp.getPrivate();
            publicKey = kp.getPublic();
            address = CryptoUtils.bytesToHex(publicKey.getEncoded());
            amount = new AtomicLong(initialAmount);
        }

        @Override
        public Transaction generateTransaction(String targetWalletAddress, long amount) {
            TransactionImpl tx = new TransactionImpl(targetWalletAddress, amount);
            tx.setSignature();
            return tx;
        }

        @Override
        public String getAddress() {
            return address;
        }

        @Override
        public PublicKey getPublicKey() {
            return publicKey;
        }

        @Override
        public long getAmount() {
            return amount.get();
        }

        @Override
        public void setAmount(long newAmount) {
            amount.set(newAmount);
        }

        class TransactionImpl implements Transaction {
            private String txID;
            private byte[] signature;
            private final String senderAddress;
            private final String recipientAddress;
            private final Instant timestamp;
            private long amount;

            TransactionImpl(String targetWalletAddress, long amount) {
                this.senderAddress = address;
                this.recipientAddress = targetWalletAddress;
                this.timestamp = Instant.now();
                this.amount = amount;
            }

            private void setSignature() {
                signature = CryptoUtils.sign(getHash(), privateKey);
            }

            @Override
            public long getAmount() {
                return amount;
            }

            @Override
            public String getRecipientAddress() {
                return recipientAddress;
            }

            @Override
            public String getOriginatorAddress() {
                return senderAddress;
            }

            @Override
            public String getHash() {
                if (txID != null) {
                    return txID;
                }
                else {
                    txID = CryptoUtils.applySha256(
                        String.join("",
                            senderAddress,
                            recipientAddress,
                            String.valueOf(amount),
                            String.valueOf(timestamp)
                        )
                    );
                }
                return txID;
            }

            @Override
            public byte[] getSignature() {
                if (signature == null) {
                    throw new IllegalStateException("The transaction is not signed");
                }
                return signature;
            }

            @Override
            public String toString() {
                return "[%d] %s -> %s".formatted(amount, recipientAddress, senderAddress);
            }
        }
    }
}
