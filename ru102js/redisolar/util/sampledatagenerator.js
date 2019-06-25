const generateHistorical = (days) => {
  if (days < 1 || days > 365) {
    throw { error: `Historical data requests must be for 1-365 days, not ${days}` };
  }

  console.log(`Generating ${days} of sample historical data.`);
};

console.log('TODO: sampledatagenerator');

try {
  const days = 1;
  generateHistorical(days);
} catch (e) {
  console.error('Error generating historical data:');
  console.error(e);
}
