pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/math/SafeMath.sol";

contract MemToken is ERC721Full {
    using SafeMath for uint256;

    address public contractOwner;

    struct Trait {
        string name;
        uint256 Price;
        uint256 maxSupply;
        uint256 mintedCount;
    }

    Trait[] public traits;

    constructor() public ERC721Full("MemToken", "WINE") {
        contractOwner = msg.sender;

        // Initialize the traits array in the constructor
        traits.push(Trait({name: "Russian River Valley", Price: 0.2 ether, maxSupply: 100, mintedCount: 0}));
        traits.push(Trait({name: "Napa Valley", Price: 0.6 ether, maxSupply: 100, mintedCount: 0}));
        traits.push(Trait({name: "Oregon", Price: 0.3 ether, maxSupply: 100, mintedCount: 0}));
        traits.push(Trait({name: "Columbia Valley", Price: 0.4 ether, maxSupply: 100, mintedCount: 0}));
        traits.push(Trait({name: "Finger Lakes", Price: 0.5 ether, maxSupply: 100, mintedCount: 0}));
    }

    mapping(uint256 => uint256) public tokenToTrait;

    function generateTokenURI(uint256 tokenId) internal view returns (string memory) {
        require(tokenId < totalSupply(), "Token does not exist");
        uint256 traitIndex = tokenToTrait[tokenId];
        Trait memory trait = traits[traitIndex];
        return string(abi.encodePacked(trait.name, "-", tokenId));
    }

    function mintMembership(address owner, uint256 traitIndex)
        public
        payable // Allow receiving payments with the function call
        returns (uint256)
    {
        require(traitIndex < traits.length, "Invalid trait index");
        Trait storage trait = traits[traitIndex];

        require(trait.mintedCount < trait.maxSupply, "Trait supply limit reached");
        require(msg.value >= trait.Price, "Insufficient payment"); // Check if payment is sufficient

        uint256 tokenId = totalSupply();
        _mint(owner, tokenId);

        string memory tokenURI = generateTokenURI(tokenId);
        _setTokenURI(tokenId, tokenURI);

        tokenToTrait[tokenId] = traitIndex;
        trait.mintedCount++;

        // Transfer the payment to the contract owner
        address payable ownerPayable = address(uint64(contractOwner));
        ownerPayable.transfer(msg.value);

        return tokenId;
    }

    function getMembershipType(uint256 tokenId) public view returns (string memory name, uint256 Price) {
        require(tokenId < totalSupply(), "Token does not exist");
        uint256 traitIndex = tokenToTrait[tokenId];
        Trait memory trait = traits[traitIndex];
        return (trait.name, trait.Price);
    }

    function getMembershipInfo(uint256 traitIndex) public view returns (string memory name, uint256 Price, uint256 maxSupply, uint256 mintedCount) {
        require(traitIndex < traits.length, "Invalid trait index");
        Trait memory trait = traits[traitIndex];
        return (trait.name, trait.Price, trait.maxSupply, trait.mintedCount);
    }
    function getTotalPaymentReceivedByOwner() public view returns (uint256) {
        return address(uint64(contractOwner)).balance;
        }
    function getTotalPaymentReceivedByContract() public view returns (uint256) {
        return address(this).balance;
    }

}