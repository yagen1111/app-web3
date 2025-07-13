async function main() {
  const TeslaToken = await ethers.getContractFactory("TeslaToken");
  const token = await TeslaToken.deploy();

  await token.waitForDeployment();
  console.log(`TeslaToken deployed to: ${await token.getAddress()}`);

}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });

