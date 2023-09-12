pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract MemToken is ERC721Full {
    constructor() public ERC721Full("MemToken", "WINE") {}

    struct Trait {
        string name;
        string value;
        uint256 maxSupply;
        uint256 mintedCount;
    }

    Trait[] public traits;

    mapping(uint256 => uint256) public tokenToTrait;
    mapping(uint256 => uint256) public mintingTime; // Mapping to store minting timestamps

    function addTrait(string memory name, string memory value, uint256 maxSupply) public {
        traits.push(Trait(name, value, maxSupply, 0));
    }

    function generateTokenURI(uint256 tokenId) internal view returns (string memory) {
        require(tokenId < totalSupply(), "Token does not exist");
        uint256 traitIndex = tokenToTrait[tokenId];
        Trait memory trait = traits[traitIndex];
        return string(abi.encodePacked(trait.name, "-", tokenId));
    }

    function mintMembership(address owner, uint256 traitIndex)
        public
        returns (uint256)
    {
        require(traitIndex < traits.length, "Invalid trait index");
        Trait storage trait = traits[traitIndex];

        require(trait.mintedCount < trait.maxSupply, "Trait supply limit reached");

        uint256 tokenId = totalSupply();
        _mint(owner, tokenId);

        string memory tokenURI = generateTokenURI(tokenId);
        _setTokenURI(tokenId, tokenURI);

        tokenToTrait[tokenId] = traitIndex;
        trait.mintedCount++;
        mintingTime[tokenId] = now; // Store the minting timestamp

        return tokenId;
    }

    function getMembershipType(uint256 tokenId) public view returns (string memory name, string memory value) {
        require(tokenId < totalSupply(), "Token does not exist");
        uint256 traitIndex = tokenToTrait[tokenId];
        Trait memory trait = traits[traitIndex];
        return (trait.name, trait.value);
    }

    function getMembershipInfo(uint256 traitIndex) public view returns (string memory name, string memory value, uint256 maxSupply, uint256 mintedCount) {
        require(traitIndex < traits.length, "Invalid trait index");
        Trait memory trait = traits[traitIndex];
        return (trait.name, trait.value, trait.maxSupply, trait.mintedCount);
    }

    // Function to check if an NFT has expired
    function isMembershipExpired(uint256 tokenId) public view returns (bool) {
        require(tokenId < totalSupply(), "Token does not exist");
        uint256 mintTime = mintingTime[tokenId];
        return now >= mintTime + 365 days;
    }
}
