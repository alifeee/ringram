const yaml = require("js-yaml");

module.exports = function (eleventyConfig) {
  // add support for reading Yaml from `/_data`
  eleventyConfig.addDataExtension("yaml", (contents) =>
    yaml.safeLoad(contents)
  );

  eleventyConfig.addHandlebarsHelper("list", (len) => {
    return new Array(len).fill(0);
  });
};
