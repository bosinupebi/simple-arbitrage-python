//SPDX-License-Identifier: UNLICENSED
pragma solidity >= 0.8.19;




interface IERC20 {
    event Approval(address indexed owner, address indexed spender, uint value);
    event Transfer(address indexed from, address indexed to, uint value);

    function name() external view returns (string memory);
    function balanceOf(address owner) external view returns (uint);
    function allowance(address owner, address spender) external view returns (uint);
    function approve(address spender, uint value) external returns (bool);
    function transfer(address to, uint value) external returns (bool);
    function transferFrom(address from, address to, uint value) external returns (bool);
}




interface IUniswapV2Router {

    function swapExactETCForTokens(uint amountOutMin, address[] calldata path, address to, uint deadline)
        external
        payable
        returns (uint[] memory amounts);


    function swapExactETHForTokens(uint amountOutMin, address[] calldata path, address to, uint deadline)
        external
        payable
        returns (uint[] memory amounts);

    function swapTokensForExactETC(uint amountOut, uint amountInMax, address[] calldata path, address to, uint deadline)
        external
        returns (uint[] memory amounts);

    function swapExactTokensForETC(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline)
        external
        returns (uint[] memory amounts);

    function swapExactTokensForETH(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline)
    external
    returns (uint[] memory amounts);

    function swapETCForExactTokens(uint amountOut, address[] calldata path, address to, uint deadline)
        external
        payable
        returns (uint[] memory amounts);

}



contract Kabuto {
    
    address private immutable owner;
    
    address private immutable executor;

    address private etcMCRouter = 0x2d18693b77acF8F2785084B0Ae53F6e0627e4376;
     

    modifier onlyCrewMember() {
        require(msg.sender == owner || msg.sender == executor);
        _;
    }

    constructor(address _executor) {
        owner = msg.sender;
        executor = _executor;
    }

    receive() external payable {
    }



function AtomicSwap(uint _buyAmountOutMin, 
                    address[] calldata _buyPath, 
                    address _buyRouter,
                    uint _sellAmountOutMin, 
                    address [] calldata _sellPath, 
                    address _sellRouter)
    external payable onlyCrewMember()
{
    // Step 1: Buy Tokens

    

    IUniswapV2Router BUYROUTER = IUniswapV2Router(_buyRouter);

    if (_buyRouter == etcMCRouter)
    {    
        BUYROUTER.swapExactETHForTokens{value: msg.value}(_buyAmountOutMin, _buyPath, address(this), 3386112000);
    }
    else
    {
        BUYROUTER.swapExactETCForTokens{value: msg.value}(_buyAmountOutMin, _buyPath, address(this), 3386112000);
    }

    
    
    // Step 2: Sell Tokens

    IERC20 _token = IERC20(_sellPath[0]);

    require(_token.balanceOf(address(this)) > 0, "Insufficient tokens in the contract");
    
    IUniswapV2Router SELLROUTER = IUniswapV2Router(_sellRouter);
    
    _token.approve(_sellRouter, _token.balanceOf(address(this)));

    if (_sellRouter == etcMCRouter)
    {    
        SELLROUTER.swapExactTokensForETH(_token.balanceOf(address(this)), _sellAmountOutMin, _sellPath, executor, 3386112000);
    }
    else
    {
        SELLROUTER.swapExactTokensForETC(_token.balanceOf(address(this)), _sellAmountOutMin, _sellPath, executor, 3386112000);
    }


    return;
}




function WithdrawERC20(address _to, uint256 _withdrawalamount, address _tokencontract) external onlyCrewMember {
    
        IERC20 _token = IERC20(_tokencontract);

        if(_withdrawalamount != 0){
            (bool _successful) = _token.transfer(_to, _withdrawalamount);
            require(_successful);
            return;
        }
        
        uint256 _tokenBalance = _token.balanceOf(address(this));

        (bool _success) = _token.transfer(_to, _tokenBalance);
        require(_success);
        return;
}

function WithdrawETC(address payable _recipient) external onlyCrewMember {
    // Ensure that the recipient address is valid
    require(_recipient != address(0), "Invalid recipient address");

    // Transfer the contract's Ether balance to the recipient
    _recipient.transfer(address(this).balance);
}

    

}