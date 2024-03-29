const yaml = require("js-yaml");

module.exports = function (eleventyConfig) {
  // add support for reading Yaml from `/_data`
  eleventyConfig.addDataExtension("yaml", (contents) =>
    yaml.safeLoad(contents)
  );

  eleventyConfig.addHandlebarsHelper("list", (len) => {
    return new Array(len).fill(0);
  });

  eleventyConfig.addHandlebarsHelper("add", (n1, n2) => {
    return n1 + n2;
  });

  eleventyConfig.addHandlebarsHelper("eq", (n1, n2) => {
    return n1 === n2;
  });
};
