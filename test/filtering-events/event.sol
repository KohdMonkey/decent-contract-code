pragma solidity >=0.7.0 <0.9.0;

/**
 * simple contract to add and remove components
 */
contract Storage {

    mapping(uint256 => bool) whitelist;
    mapping(uint256 => bool) revocationlist;

    event add(uint256 enclaveId);
    event revoke(uint256 enclaveId);

    /**
     * initialize the whiteList with some enclave IDs
     */
    constructor() {
        whitelist[1001] = true;
        whitelist[2002] = true;
        whitelist[3003] = true;
    }
   
    /**
     * check if enclave is in whitelist
     */
    function isInWhitelist(uint256 enclaveId) public view returns (bool) {
        return whitelist[enclaveId];
    }

    /**
     * add enclave to whitelist
     */
    function addToWhitelist(uint256 enclaveId) public {
        if(!whitelist[enclaveId]) {
            whitelist[enclaveId] = true;

            emit add(enclaveId);
        }
    }

    /**
     * revoke an enclave component
     */
    function revokeEnclave(uint256 enclaveId) public {
        if(!revocationlist[enclaveId]) {
            revocationlist[enclaveId] = true;
            
            // remove from whitelist
            whitelist[enclaveId] = false;
            
            emit revoke(enclaveId);
        }
    }

}