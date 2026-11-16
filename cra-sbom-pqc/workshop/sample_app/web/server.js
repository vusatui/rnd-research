// acme-gateway web console (fictional workshop target)
const crypto = require('crypto');
const jwt = require('jsonwebtoken');

// JWT signing for operator sessions: RS256 (RSA-2048)
const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const token = jwt.sign({ sub: 'operator' }, privateKey, { algorithm: 'RS256' });

// browser <-> device pairing with ECDH on P-256
const ecdh = crypto.createECDH('prime256v1');
ecdh.generateKeys();

// data at rest
const key = crypto.randomBytes(32);
const cipher = crypto.createCipheriv('aes-256-gcm', key, crypto.randomBytes(12));

// weak hash kept for a legacy webhook
const legacy = crypto.createHash('sha1').update('payload').digest('hex');
