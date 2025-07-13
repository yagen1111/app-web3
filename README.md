# TradeTokenX

A decentralized application (DApp) that tracks Tesla stock prices on the blockchain using smart contracts and oracles. The project includes an ERC20 token that stores Tesla's real-time stock price data.

## 🏗️ Architecture

TradeTokenX consists of three main components:

1. **Smart Contracts** - ERC20 token contract with price oracle functionality
2. **Oracle Backend** - Python service that fetches Tesla stock prices and updates the blockchain
3. **Frontend** - React application for interacting with the smart contract
4. **CI/CD Pipeline** - Automated testing and deployment workflows

## 📁 Project Structure

```
TradeTokenX/
├── .github/workflows/     # CI/CD pipeline configuration
├── smart-contracts/       # Hardhat project with Solidity contracts
├── frontend/              # React frontend application
├── oracle-backend/        # Python oracle service
└── README.md             # This file
```

## 🚀 Features

- **Tesla Token (TSLA)** - ERC20 token with real-time price tracking
- **Price Oracle** - Automated price updates from Yahoo Finance API
- **Smart Contract Integration** - Secure on-chain price storage
- **CI/CD Pipeline** - Automated testing and deployment
- **Multi-environment Support** - Development, staging, and production configurations

## 🛠️ Technology Stack

### Smart Contracts
- **Solidity** ^0.8.20
- **Hardhat** - Development framework
- **OpenZeppelin** - Secure contract libraries
- **Sepolia Testnet** - Ethereum test network

### Oracle Backend
- **Python** 3.9+
- **Web3.py** - Ethereum interaction
- **Requests** - HTTP client for API calls
- **Yahoo Finance API** - Tesla stock price data

### Frontend
- **React** - User interface framework
- **Node.js** 18+ - JavaScript runtime

### DevOps
- **GitHub Actions** - CI/CD automation
- **Vercel** - Frontend deployment
- **npm** - Package management

## 📋 Prerequisites

Before running this project, ensure you have:

- **Node.js** 18+ installed
- **Python** 3.9+ installed
- **Git** for version control
- **MetaMask** or similar Web3 wallet
- **Sepolia ETH** for testnet transactions

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd TradeTokenX
```

### 2. Smart Contracts Setup

```bash
cd smart-contracts
npm install

# Create environment file
cp .env.example .env
# Edit .env with your credentials:
# - PRIVATE_KEY: Your wallet private key
# - ALCHEMY_API_KEY: Your Alchemy API key
```

### 3. Deploy Smart Contract

```bash
# Compile contracts
npx hardhat compile

# Deploy to Sepolia testnet
npx hardhat run scripts/deploy.js --network sepolia

# Run tests
npx hardhat test
```

### 4. Oracle Backend Setup

```bash
cd ../oracle-backend
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with:
# - PRIVATE_KEY: Same as smart contracts
# - ALCHEMY_API_KEY: Same as smart contracts
# - UPDATE_INTERVAL: Price update frequency (seconds)

# Run the oracle
python tesla_oracle.py
```

### 5. Frontend Setup

```bash
cd ../frontend
npm install

# Configure contract address
# Update REACT_APP_CONTRACT_ADDRESS in .env with deployed contract address

# Start development server
npm start
```

## 🔧 Configuration

### Environment Variables

#### Smart Contracts & Oracle (.env)
```bash
PRIVATE_KEY=your_metamask_private_key_here
ALCHEMY_API_KEY=your_alchemy_api_key_here
UPDATE_INTERVAL=300  # Price update interval in seconds
```

#### Frontend (.env)
```bash
REACT_APP_CONTRACT_ADDRESS=0x16D093BDa86814561C2BdC99d39b32A10e9D4F09
```

### Contract Configuration

The Tesla Token contract is deployed at:
- **Sepolia Testnet**: `0x16D093BDa86814561C2BdC99d39b32A10e9D4F09`

## 📊 Smart Contract Details

### TeslaToken Contract

```solidity
// Key Functions:
- updatePrice(uint256 newPriceUSD) - Updates Tesla stock price (owner only)
- getPriceUSD() - Returns current Tesla price in cents
- Standard ERC20 functions (transfer, approve, etc.)

// Token Details:
- Name: "Tesla Token"
- Symbol: "TSLA"
- Initial Supply: 1,000 tokens
- Price Storage: USD cents (e.g., $245.67 = 24567)
```

## 🤖 Oracle Service

The Python oracle service:

1. **Fetches** Tesla stock price from Yahoo Finance API
2. **Converts** price to cents (removes decimals)
3. **Updates** smart contract via blockchain transaction
4. **Runs** continuously with configurable intervals

### Oracle Features
- **Automatic Price Updates** - Configurable update frequency
- **Error Handling** - Robust error handling and retry logic
- **Transaction Optimization** - Skips updates if price unchanged
- **Logging** - Detailed logging for monitoring

## 🧪 Testing

### Smart Contract Tests
```bash
cd smart-contracts
npx hardhat test
npx hardhat coverage
```

### Oracle Tests
```bash
cd oracle-backend
python -m pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

## 🚀 Deployment

### Automated Deployment (Recommended)

The project includes GitHub Actions for automated deployment:

1. **Push to `develop`** branch → Deploy to staging
2. **Push to `main`** branch → Deploy to production
3. **Pull requests** → Run full test suite

### Manual Deployment

#### Smart Contracts
```bash
npx hardhat run scripts/deploy.js --network sepolia
```

#### Frontend (Vercel)
```bash
npm run build
# Deploy build/ directory to Vercel
```

## 📈 Monitoring

### Oracle Monitoring
The oracle provides detailed logging:
- Price fetch status
- Transaction confirmations
- Error messages
- Update intervals

### Contract Monitoring
Monitor contract interactions on:
- **Sepolia Etherscan**: https://sepolia.etherscan.io/
- **Alchemy Dashboard**: Monitor API usage

## 🔒 Security Considerations

1. **Private Keys** - Never commit private keys to version control
2. **Environment Variables** - Use `.env` files for sensitive data
3. **Contract Ownership** - Only contract owner can update prices
4. **API Rate Limits** - Respect Yahoo Finance API rate limits
5. **Gas Optimization** - Oracle skips unnecessary transactions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Workflow

1. **Make changes** in appropriate directory
2. **Run tests** to ensure functionality
3. **Update documentation** if needed
4. **Submit PR** with clear description

## 📚 API Reference

### Smart Contract ABI

Key contract functions:
```javascript
// Read Functions
getPriceUSD() → uint256

// Write Functions (Owner Only)
updatePrice(uint256 newPriceUSD)

// Standard ERC20 Functions
transfer(address to, uint256 amount)
approve(address spender, uint256 amount)
balanceOf(address account) → uint256
```

### Oracle API Integration

The oracle fetches data from:
- **Yahoo Finance API**: `https://query1.finance.yahoo.com/v8/finance/chart/TSLA`

## 🐛 Troubleshooting

### Common Issues

1. **"Insufficient funds" error**
   - Ensure wallet has Sepolia ETH
   - Check gas prices

2. **"Oracle not updating prices"**
   - Verify API connectivity
   - Check private key configuration
   - Monitor gas prices

3. **"Frontend not connecting"**
   - Verify MetaMask is connected
   - Check contract address configuration
   - Ensure correct network (Sepolia)

4. **"Contract deployment fails"**
   - Verify network configuration
   - Check Alchemy API key
   - Ensure sufficient gas

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenZeppelin** - Secure smart contract libraries
- **Hardhat** - Ethereum development environment
- **Yahoo Finance** - Stock price data API
- **Alchemy** - Ethereum infrastructure
- **Vercel** - Frontend hosting platform

## 📞 Support

For support and questions:
- Create an issue in this repository
- Check existing documentation
- Review troubleshooting guide

---

**⚠️ Disclaimer**: This project is for educational and demonstration purposes. Not intended for production financial applications without proper security audits.
