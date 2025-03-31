// Define scoring systems
const individualPoints = [20, 17, 16, 15, 14, 13, 12, 11, 9, 7, 6, 5, 4, 3, 2, 1];
const relayPoints = [40, 34, 32, 30, 28, 26, 24, 22, 18, 14, 12, 10, 8, 6, 4, 2];

// Initialize team scores
const teamScores = {};
const ageGroupScores = {
  '10&U': {},
  '11-12': {},
  '13-14': {}
};

// Helper function to add points to a team
function addPoints(team, points, ageGroup = null) {
  // Extract team code without the "MD" suffix
  team = team.split('-')[0];
  
  if (!teamScores[team]) {
    teamScores[team] = 0;
  }
  teamScores[team] += points;
  
  // Add to age group scoring if specified
  if (ageGroup) {
    if (!ageGroupScores[ageGroup][team]) {
      ageGroupScores[ageGroup][team] = 0;
    }
    ageGroupScores[ageGroup][team] += points;
  }
}

// Function to process an event
function processEvent(eventName, teams, isRelay, ageGroup) {
  const pointSystem = isRelay ? relayPoints : individualPoints;
  
  for (let i = 0; i < teams.length && i < 16; i++) {
    if (teams[i]) {
      addPoints(teams[i], pointSystem[i], ageGroup);
    }
  }
}

// Define more events - I'll create a significantly larger sample to improve accuracy

// 13-14 AGE GROUP EVENTS
// Top teams from various events based on seeding from psych sheet
const events1314 = [
  // Relays
  {
    name: "Girls 13-14 200 Medley Relay (#1)",
    teams: ["NBAC-MD", "ASC-MD", "EST-MD", "FSC-MD", "LBA-MD", "NAAC-MD", "SPRC-MD", "ACA-MD", "BAY-MD", "OPST-MD", "SMDA-MD", "CAA-MD", "RAC-MD", "MAC-MD"],
    isRelay: true
  },
  {
    name: "Boys 13-14 200 Medley Relay (#2)",
    teams: ["NBAC-MD", "NAAC-MD", "CAA-MD", "EST-MD", "CAC-MD", "FSC-MD", "MAC-MD", "RAC-MD", "BAY-MD", "LBA-MD", "SMDA-MD"],
    isRelay: true
  },
  {
    name: "Girls 13-14 800 Free Relay (#15)",
    teams: ["NBAC-MD", "EST-MD", "ASC-MD", "FSC-MD", "LBA-MD", "SPRC-MD"],
    isRelay: true
  },
  {
    name: "Boys 13-14 800 Free Relay (#16)",
    teams: ["NAAC-MD", "NBAC-MD", "CAA-MD", "EST-MD", "FSC-MD", "CAC-MD", "MAC-MD", "LBA-MD"],
    isRelay: true
  },
  
  // Distance Freestyle
  {
    name: "Girls 13-14 1000 Free (#7)",
    teams: ["NBAC-MD", "MAC-MD", "EST-MD", "NAAC-MD", "HFY-MD", "OPST-MD"],
    isRelay: false
  },
  {
    name: "Boys 13-14 1000 Free (#8)",
    teams: ["NBAC-MD", "LBA-MD", "NBAC-MD", "NBAC-MD", "EST-MD", "NBAC-MD", "ASC-MD", "MAC-MD", "NAAC-MD", "CAA-MD", "BAY-MD", "LBA-MD"],
    isRelay: false
  },
  {
    name: "Girls 13-14 500 Free (#29)",
    teams: ["NBAC-MD", "LBA-MD", "NBAC-MD", "EST-MD", "NAAC-MD", "EST-MD", "MAC-MD", "EST-MD", "NBAC-MD", "EST-MD", "NBAC-MD", "EST-MD", "NBAC-MD", "NAAC-MD", "SPRC-MD", "NBAC-MD"],
    isRelay: false
  },
  {
    name: "Boys 13-14 500 Free (#30)",
    teams: ["NAAC-MD", "NBAC-MD", "NAAC-MD", "NBAC-MD", "NBAC-MD", "NBAC-MD", "FSC-MD", "EST-MD", "TCY-MD", "OPST-MD", "NBAC-MD", "FSC-MD", "NBAC-MD", "CAA-MD", "BAY-MD", "NBAC-MD"],
    isRelay: false
  },
  
  // IM Events
  {
    name: "Girls 13-14 100 IM (#9)",
    teams: ["NBAC-MD", "NBAC-MD", "EST-MD", "NBAC-MD", "NBAC-MD", "NBAC-MD", "ASC-MD", "ACA-MD", "NBAC-MD", "NBAC-MD", "ASC-MD", "EST-MD", "ROCK-MD", "EST-MD", "ACA-MD", "LBA-MD"],
    isRelay: false
  },
  {
    name: "Boys 13-14 100 IM (#10)",
    teams: ["NAAC-MD", "NAAC-MD", "NBAC-MD", "NBAC-MD", "NBAC-MD", "CAA-MD", "EST-MD", "FSC-MD", "NBAC-MD", "NAAC-MD", "NBAC-MD", "NBAC-MD", "NBAC-MD", "NAAC-MD", "MAC-MD", "NBAC-MD"],
    isRelay: false
  },
  {
    name: "Girls 13-14 200 IM (#51)",
    teams: ["NBAC-MD", "NBAC-MD", "NBAC-MD", "EST-MD", "NBAC-MD", "NBAC-MD", "NBAC-MD", "NAAC-MD", "NBAC-MD", "EST-MD", "NBAC-MD", "EST-MD", "NBAC-MD", "NAAC-MD", "ASC-MD", "NBAC-MD"],
    isRelay: false
  },
  {
    name: "Boys 13-14 200 IM (#52)",
    teams: ["NBAC-MD", "NAAC-MD", "NBAC-MD", "NBAC-MD", "NBAC-MD", "NAAC-MD", "CAC-MD", "NAAC-MD", "TCY-MD", "OPST-MD", "NBAC-MD", "EST-MD", "NBAC-MD", "FSC-MD", "EST-MD", "FSC-MD"],
    isRelay: false
  },
  
  // Backstroke
  {
    name: "Girls 13-14 50 Back (#17)",
    teams: ["EST-MD", "NBAC-MD", "RAC-MD", "NBAC-MD", "ASC-MD", "NBAC-MD", "ACA-MD", "LBA-MD", "SPRC-MD", "BAY-MD", "FSC-MD", "EST-MD", "NBAC-MD", "MAC-MD", "EST-MD", "CAA-MD"],
    isRelay: false
  },
  {
    name: "Boys 13-14 50 Back (#18)",
    teams: ["NBAC-MD", "NAAC-MD", "NBAC-MD", "NBAC-MD", "CAA-MD", "NBAC-MD", "NBAC-MD", "NAAC-MD", "NBAC-MD", "FSC-MD", "MAC-MD", "NBAC-MD", "CAA-MD", "MAC-MD", "MAC-MD", "NBAC-MD"],
    isRelay: false
  },
  {
    name: "Girls 13-14 100 Back (#69)",
    teams: ["EST-MD", "LBA-MD", "NBAC-MD", "RAC-MD", "SPRC-MD", "LBA-MD", "EST-MD", "ACA-MD", "FSC-MD", "BAY-MD", "NAAC-MD", "NBAC-MD", "EST-MD", "NBAC-MD", "ASC-MD", "NBAC-MD"],
    isRelay: false
  },
  {
    name: "Boys 13-14 100 Back (#70)",
    teams: ["NAAC-MD", "NAAC-MD", "NBAC-MD", "NBAC-MD", "NBAC-MD", "FSC-MD", "TCY-MD", "NAAC-MD", "NBAC-MD", "FSC-MD", "MAC-MD", "FSC-MD", "NBAC-MD", "FSC-MD", "CAA-MD", "EST-MD"],
    isRelay: false
  },
  
  // Breaststroke
  {
    name: "Girls 13-14 50 Breast (#105)",
    teams: ["NBAC-MD", "ASC-MD", "NBAC-MD", "NBAC-MD", "ASC-MD", "OPST-MD", "ASC-MD", "ASC-MD", "FSC-MD", "NAAC-MD", "NAAC-MD", "FSC-MD", "EST-MD", "HFY-MD", "NBAC-MD", "BAY-MD"],
    isRelay: false
  },
  {
    name: "Boys 13-14 50 Breast (#106)",
    teams: ["NBAC-MD", "NBAC-MD", "NBAC-MD", "EST-MD", "NBAC-MD", "NAAC-MD", "CAC-MD", "NAAC-MD", "RAC-MD", "CAA-MD", "NBAC-MD", "NBAC-MD", "CAA-MD", "JCC-MD", "GTAC-MD", "NBAC-MD"],
    isRelay: false
  },
  {
    name: "Girls 13-14 100 Breast (#23)",
    teams: ["NBAC-MD", "NBAC-MD", "NBAC-MD", "NBAC-MD", "ASC-MD", "OPST-MD", "FSC-MD", "ASC-MD", "NAAC-MD", "FSC-MD", "ASC-MD", "NBAC-MD", "CAA-MD", "LBA-MD", "NBAC-MD", "BAY-MD"],
    isRelay: false
  },
  {
    name: "Boys 13-14 100 Breast (#24)",
    teams: ["NBAC-MD", "EST-MD", "NBAC-MD", "NBAC-MD", "NBAC-MD", "FSC-MD", "NAAC-MD", "CAA-MD", "CAC-MD", "FSC-MD", "CAA-MD", "CAA-MD", "CAA-MD", "NBAC-MD", "HFY-MD", "RAC-MD"],
    isRelay: false
  }
];

// 11-12 AGE GROUP EVENTS
const events1112 = [
  // Relays
  {
    name: "Girls 11-12 200 Medley Relay (#13)",
    teams: ["NBAC-MD", "FSC-MD", "MAC-MD", "ASC-MD", "CAA-MD", "BAY-MD", "EST-MD", "GBSA-MD"],
    isRelay: true
  },
  {
    name: "Boys 11-12 200 Medley Relay (#14)",
    teams: ["NBAC-MD", "LBA-MD", "FSC-MD", "CAA-MD", "BAY-MD", "ASC-MD", "MAC-MD"],
    isRelay: true
  },
  
  // Freestyle
  {
    name: "Girls 11-12 500 Free (#5)",
    teams: ["OPST-MD", "ASC-MD", "FSC-MD", "ASC-MD", "FSC-MD", "NBAC-MD"],
    isRelay: false
  },
  {
    name: "Boys 11-12 500 Free (#6)",
    teams: ["NBAC-MD", "SPRC-MD", "LBA-MD", "CAA-MD", "LBA-MD", "YCM-MD", "MAC-MD", "NBAC-MD", "MAC-MD"],
    isRelay: false
  },
  {
    name: "Girls 11-12 100 Free (#31)",
    teams: ["FSC-MD", "CAA-MD", "SPRC-MD", "OPST-MD", "CAA-MD", "NBAC-MD", "NBAC-MD", "FSC-MD", "RAC-MD", "NBAC-MD", "FAST-MD", "NAAC-MD", "MAC-MD", "MAC-MD", "FSC-MD", "BAY-MD"],
    isRelay: false
  },
  {
    name: "Boys 11-12 100 Free (#32)",
    teams: ["NBAC-MD", "EST-MD", "EST-MD", "NBAC-MD", "LBA-MD", "ASC-MD", "HAWK-MD", "GBSA-MD", "LBA-MD", "HAWK-MD", "NBAC-MD", "LBA-MD", "FSC-MD", "YCM-MD", "NBAC-MD", "ASC-MD"],
    isRelay: false
  },
  
  // IM Events
  {
    name: "Girls 11-12 100 IM (#59)",
    teams: ["FSC-MD", "MAC-MD", "FSC-MD", "NAAC-MD", "RAC-MD", "NBAC-MD", "NBAC-MD", "MAC-MD", "CAA-MD", "NBAC-MD", "NBAC-MD", "CAA-MD", "MAC-MD", "FSC-MD", "GBSA-MD", "CAC-MD"],
    isRelay: false
  },
  {
    name: "Boys 11-12 100 IM (#60)",
    teams: ["NBAC-MD", "EST-MD", "NBAC-MD", "LBA-MD", "CAA-MD", "EST-MD", "SMDA-MD", "LBA-MD", "HAWK-MD", "ASC-MD", "FSC-MD", "ASC-MD", "CAA-MD", "YCM-MD", "CAA-MD", "MAC-MD"],
    isRelay: false
  },
  
  // Backstroke
  {
    name: "Girls 11-12 100 Back (#95)",
    teams: ["FSC-MD", "MAC-MD", "FSC-MD", "NAAC-MD", "RAC-MD", "NBAC-MD", "FSC-MD", "GBSA-MD", "FAST-MD", "GBSA-MD", "MAC-MD", "FSC-MD", "EST-MD", "EST-MD", "NBAC-MD", "OPST-MD"],
    isRelay: false
  },
  {
    name: "Boys 11-12 100 Back (#96)",
    teams: ["NBAC-MD", "EST-MD", "SPRC-MD", "CAA-MD", "NBAC-MD", "FSC-MD", "LBA-MD", "EST-MD", "NBAC-MD", "NBAC-MD", "FSC-MD", "HAWK-MD", "NBAC-MD", "NBAC-MD", "ASC-MD", "MAC-MD"],
    isRelay: false
  }
];

// 10 & UNDER AGE GROUP EVENTS
const events10U = [
  // Relays
  {
    name: "Girls 10&U 200 Medley Relay (#11)",
    teams: ["NBAC-MD", "ASC-MD", "EST-MD", "BAY-MD", "MAC-MD", "SPRC-MD", "LBA-MD", "FSC-MD", "CAC-MD", "CAA-MD", "NAAC-MD"],
    isRelay: true
  },
  {
    name: "Boys 10&U 200 Medley Relay (#12)",
    teams: ["LBA-MD", "ASC-MD", "CAA-MD", "FSC-MD", "BAY-MD", "NBAC-MD", "NAAC-MD", "SMDA-MD"],
    isRelay: true
  },
  
  // Freestyle
  {
    name: "Girls 10&U 500 Free (#3)",
    teams: ["NBAC-MD", "NBAC-MD", "CAA-MD", "NBAC-MD", "FSC-MD", "CAC-MD"],
    isRelay: false
  },
  {
    name: "Boys 10&U 500 Free (#4)",
    teams: ["NBAC-MD", "CAA-MD", "ASC-MD", "LBA-MD", "LBA-MD", "MAS-MD", "CAA-MD", "NBAC-MD"],
    isRelay: false
  },
  {
    name: "Girls 10&U 100 Free (#27)",
    teams: ["NBAC-MD", "NBAC-MD", "CAA-MD", "BAY-MD", "NBAC-MD", "EST-MD", "FSC-MD", "EST-MD", "ASC-MD", "HAGY-MD", "ACA-MD", "BAY-MD", "LBA-MD", "MAC-MD", "CAA-MD", "YCM-MD"],
    isRelay: false
  },
  {
    name: "Boys 10&U 100 Free (#28)",
    teams: ["NBAC-MD", "MBK-MD", "ASC-MD", "LBA-MD", "LBA-MD", "ASC-MD", "CGA-MD", "CAA-MD", "EST-MD", "CAA-MD", "BAY-MD", "ASC-MD", "BAY-MD", "FAST-MD", "SMDA-MD", "NAAC-MD"],
    isRelay: false
  },
  
  // IM Events
  {
    name: "Girls 10&U 200 IM (#39)",
    teams: ["NBAC-MD", "NBAC-MD", "EST-MD", "CAA-MD", "ASC-MD", "ASC-MD", "FSC-MD", "SPRC-MD", "BAY-MD", "NBAC-MD", "NBAC-MD", "EST-MD", "HAGY-MD", "LBA-MD", "HAGY-MD", "CAA-MD"],
    isRelay: false
  },
  {
    name: "Boys 10&U 200 IM (#40)",
    teams: ["NBAC-MD", "ASC-MD", "NAAC-MD", "MBK-MD", "NAAC-MD", "ASC-MD", "CGA-MD", "CAA-MD", "CGA-MD", "YCM-MD", "BAY-MD", "RAC-MD", "BAY-MD", "FAST-MD", "CAA-MD", "MBK-MD"],
    isRelay: false
  },
  
  // Backstroke
  {
    name: "Girls 10&U 100 Back (#91)",
    teams: ["NBAC-MD", "NBAC-MD", "CAA-MD", "ASC-MD", "ASC-MD", "NBAC-MD", "FSC-MD", "BAY-MD", "LBA-MD", "HAGY-MD", "SPRC-MD", "MAC-MD", "FSC-MD", "ASC-MD", "EST-MD", "CAC-MD"],
    isRelay: false
  },
  {
    name: "Boys 10&U 100 Back (#92)",
    teams: ["NBAC-MD", "ASC-MD", "ASC-MD", "LBA-MD", "CAA-MD", "MBK-MD", "LBA-MD", "MAC-MD", "LBA-MD", "CAA-MD", "BAY-MD", "BAY-MD", "CAA-MD", "CGA-MD", "LBA-MD", "SMDA-MD"],
    isRelay: false
  }
];

// Process all events
console.log("Processing 13-14 events...");
events1314.forEach(event => {
  processEvent(event.name, event.teams, event.isRelay, '13-14');
});

console.log("Processing 11-12 events...");
events1112.forEach(event => {
  processEvent(event.name, event.teams, event.isRelay, '11-12');
});

console.log("Processing 10&U events...");
events10U.forEach(event => {
  processEvent(event.name, event.teams, event.isRelay, '10&U');
});

// Display overall team scores
console.log("\nPROJECTED OVERALL TEAM STANDINGS:");
const sortedTeams = Object.entries(teamScores)
  .sort((a, b) => b[1] - a[1])
  .map(([team, score], index) => `${index + 1}. ${team}: ${score} points`);

console.log(sortedTeams.join('\n'));

// Display age group scores
for (const ageGroup in ageGroupScores) {
  console.log(`\n${ageGroup} AGE GROUP STANDINGS:`);
  const sortedAgeGroup = Object.entries(ageGroupScores[ageGroup])
    .sort((a, b) => b[1] - a[1])
    .map(([team, score], index) => `${index + 1}. ${team}: ${score} points`);
  
  console.log(sortedAgeGroup.join('\n'));
}

// Generate a summary table for top 10 teams with columns for each age group
console.log("\nTOP 10 TEAMS BREAKDOWN BY AGE GROUP:");
console.log("Rank Team    Total  10&U  11-12  13-14");
console.log("-----------------------------------------");

const top10Teams = Object.entries(teamScores)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 10);

top10Teams.forEach(([team, total], index) => {
  const tenUnder = ageGroupScores['10&U'][team] || 0;
  const elevenTwelve = ageGroupScores['11-12'][team] || 0;
  const thirteenFourteen = ageGroupScores['13-14'][team] || 0;
  
  console.log(`${(index + 1).toString().padEnd(4)} ${team.padEnd(7)} ${total.toString().padEnd(6)} ${tenUnder.toString().padEnd(5)} ${elevenTwelve.toString().padEnd(6)} ${thirteenFourteen}`);
});

console.log("\nNote: This analysis is based on a sampling of events from the psyche sheet.");
console.log("The projection assumes swimmers finish according to their seedings.");
console.log("Actual results may vary depending on performance on the day of the meet.");