import Web3 from "web3";
import detectEthereumProvider from "@metamask/detect-provider";

const getWeb3 = () =>
  new Promise((resolve, reject) => {

    // Wait for loading completion to avoid race conditions with web3 injection timing.
    window.addEventListener("load", async () => {

      const provider = await detectEthereumProvider();

      if (provider) {

        provider.request({ method: "eth_requestAccounts" });
        
        const web3 = new Web3(provider)

        resolve(web3)
        // on changing the metamask accounts reload the website. 
        window.ethereum.on('accountsChanged', () => {
        window.location.reload();

        });
      } else {
        console.error("Please install MetaMask!");
      }

    });
  });

export default getWeb3;
