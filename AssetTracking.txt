// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.2;

contract AssetTracking{
    
    enum AssetOwner {TCS, CUSTOMER, PERSONAL}
    enum SOE {TCS, CUSTOMER}
    enum AssetType {LAPTOP, DESKTOP, THINCLIENT, OTHERS}
    enum LocationType {OFFICE, HOME, OTHERS}
    
    bool ModelMLreadiness;
    
    address projectOwner;
    address[] operators;
    mapping(address => bool) operatorOf;
    
    
    struct AssetLocation{
        bytes32 latitude;
        bytes32 longitude;
        bytes32 streetName;
        bytes32 cityName;
        bytes32 stateName;
        uint256 pincode;
        LocationType locationType;
    }
    
    struct AssetLoggings{
        uint256 timestamp;
        bytes32 softwareName;
        bool logginInfo; // True : Login, False : Logout
        bytes32 memo;
        AssetLocation assetLocation;
    }
    
    struct Asset{
        uint256 nonce;
        bytes32 assetId;
        bytes32 macId;
        AssetOwner assetOwner;
        SOE soe;
        AssetType assetType;
        mapping(uint256 => AssetLoggings) assetloggings; // uint256 is nonce
    }
    
    struct LocationIdentifier{
        bytes32 latitude;
        bytes32 longitude;
        uint256 radius;
        LocationType identifiedLocation;
    }
    mapping(uint256 => LocationIdentifier) locationUpdator; // here uint256 is asset number.
    mapping(bytes => LocationType) fetchLocation;
    
    Asset[] assets;
    uint256 assetNumber = 0;
    
    mapping(uint256=> mapping(uint256 => uint256)) empAssets; // empAssets[empId][empAssetNo] = assetNumber
    mapping(bytes32 => bytes32) assetOf; // assetOf[macId] = assetId
    mapping(bytes32 => uint256) assetNumberOf; // assetNumberOf[assetId] = assetNumber
    mapping(uint256 => uint256) empIdOf; // empIdOf[assetNumber] = empId
    mapping(uint256 => uint256) empAssetNoOf; // empAssetNoOf[assetNumber] = empAssetNo.
    
    modifier onlyProjectOwner {
        require(
            msg.sender == projectOwner,
            "Only owner can call this function."
        );
        _;
    }
    
    modifier onlyOperator{
        require(
            operatorOf[msg.sender]==true,
            "only operator can execute this function."
        );
        _;
    }
    
    constructor(address[] memory _operators){
        projectOwner = msg.sender;
        operators = _operators;
        for(uint8 i=0;i<_operators.length;i++){
            operatorOf[_operators[i]]=true;
        }
    }
    
    function insertAssetDetails(bytes32 _assetId, uint256 _empId, uint256 _empAssetNo, bytes32 _macId, uint256 _assetOwner, uint256 _soe, uint256 _assetType) public onlyOperator{
        empAssets[_empId][_empAssetNo] = assetNumber;
        assets[assetNumber].assetId = _assetId;
        assets[assetNumber].macId = _macId;
        assets[assetNumber].assetOwner = AssetOwner(_assetOwner);
        assets[assetNumber].soe = SOE(_soe);
        assets[assetNumber].assetType = AssetType(_assetType);
        assets[assetNumber].nonce = 0;
        
        assetOf[_macId] = _assetId;
        assetNumberOf[_assetId] = assetNumber;
        empIdOf[assetNumber] = _empId;
        empAssetNoOf[assetNumber] = _empAssetNo;
        assetNumber = assetNumber + 1;
    }
    
    function fetchAssetIdFromMACId(bytes32 _macId) internal view returns(bytes32 _assetId){
        return assetOf[_macId];
    }
    
    function fetchAssetNumberFromAssetId(bytes32 _assetId) internal view returns(uint256 _assetNo){
        return assetNumberOf[_assetId];
    }
    
    function fetchEmpIdFromAssetNumber(uint256 _assetNo) internal view returns(uint256 _empId){
        return empIdOf[_assetNo];
    }
    
    function fetchEmpAssetNoFromAssetNumber(uint256 _assetNo) internal view returns(uint256 _empAssetNo){
        return empAssetNoOf[_assetNo];
    }
    
    function fetchAssetNumberFromMACId(bytes32 _macId) internal view returns(uint256){
        bytes32 _assetId = fetchAssetIdFromMACId(_macId);
        uint256 _assetNo = fetchAssetNumberFromAssetId(_assetId);
        return _assetNo;
    }
    
    function fetchEmpIdFromMACId(bytes32 _macId) internal view returns(uint256){
        uint256 _assetNo = fetchAssetNumberFromMACId(_macId);
        return empIdOf[_assetNo];
    }
    
    function updateLocationType(uint256 _assetNo, uint256 _locType, uint256 _radius, bytes32 _latitude, bytes32 _longitude)internal onlyProjectOwner onlyOperator{
        locationUpdator[_assetNo].latitude = _latitude;
        locationUpdator[_assetNo].longitude = _longitude;
        locationUpdator[_assetNo].radius = _radius;
        locationUpdator[_assetNo].identifiedLocation = LocationType(_locType);
        bytes memory index = abi.encodePacked(_assetNo, _latitude, _longitude);
        fetchLocation[index] = locationUpdator[_assetNo].identifiedLocation;
    }
    
    function updateModelReadiness(bool data)internal onlyProjectOwner onlyOperator{
        ModelMLreadiness = data;
    }
    
    function fetchLocationType(uint256 _assetNo, bytes32 _latitude, bytes32 _longitude)internal view returns(LocationType){
        if(ModelMLreadiness){
            bytes memory index = abi.encodePacked(_assetNo, _latitude, _longitude);
            return fetchLocation[index];
        }else{
            return LocationType.OTHERS;
        }
    }
    
    function updateAssetLoggingsFromMACId(bytes32 _macId, uint256 _now, bytes32 _softwareName, bytes32 _memo, bytes32 _latitude, bytes32 _longitude, bytes32 _streetName, bytes32 _cityName, bytes32 _stateName, uint256 _pincode) internal{
        uint256 _assetNo = fetchAssetNumberFromMACId(_macId);
        uint256 nonce = assets[_assetNo].nonce;
        assets[_assetNo].assetloggings[nonce].timestamp = _now;
        assets[_assetNo].assetloggings[nonce].softwareName = _softwareName;
        assets[_assetNo].assetloggings[nonce].memo = _memo;
        assets[_assetNo].assetloggings[nonce].assetLocation.latitude = _latitude;
        assets[_assetNo].assetloggings[nonce].assetLocation.longitude = _longitude;
        assets[_assetNo].assetloggings[nonce].assetLocation.streetName = _streetName;
        assets[_assetNo].assetloggings[nonce].assetLocation.cityName = _cityName;
        assets[_assetNo].assetloggings[nonce].assetLocation.stateName = _stateName;
        assets[_assetNo].assetloggings[nonce].assetLocation.pincode = _pincode;
        assets[_assetNo].assetloggings[nonce].assetLocation.locationType = LocationType(fetchLocationType(_assetNo,_latitude,_longitude));
    }
    
    function transferProjectControl(address _to) public onlyProjectOwner{
        require(_to != address(0),"address of project owner should be valid");
        projectOwner = _to;
    }
    
    function trackAssetByAssetNumber(uint256 _assetNo)internal view onlyOperator returns(Asset storage) {
        return assets[_assetNo];
    }
    
}






