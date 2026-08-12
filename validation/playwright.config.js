const { defineConfig } = require('@playwright/test');
module.exports=defineConfig({testDir:'./playwright/specs',timeout:60000,use:{baseURL:process.env.AVF_BASE_URL,headless:true,screenshot:'only-on-failure',trace:'retain-on-failure',video:'retain-on-failure'},projects:[{name:'chromium',use:{browserName:'chromium'}}]});
