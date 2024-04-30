const yaml = require("js-yaml");
const htmlmin = require("html-minifier");

module.exports = function (eleventyConfig) {
  // copy static files
  eleventyConfig.addPassthroughCopy({ public: "/" });

  // add support for reading Yaml from `/_data`
  eleventyConfig.addDataExtension("yaml", (contents) =>
    yaml.safeLoad(contents)
  );

  eleventyConfig.addHandlebarsHelper("json", (obj) => {
    return JSON.stringify(obj);
  });

  eleventyConfig.addHandlebarsHelper("list", (len) => {
    return new Array(len).fill(0);
  });

  eleventyConfig.addHandlebarsHelper("flatten", (arr) => {
    return arr.flat();
  });

  eleventyConfig.addHandlebarsHelper("getindex", (arr, ind) => {
    return arr[ind];
  });

  eleventyConfig.addHandlebarsHelper("length", (arr) => {
    return arr.length;
  });

  eleventyConfig.addHandlebarsHelper("strToList", (s) => {
    return s.split("");
  });

  eleventyConfig.addHandlebarsHelper("add", (n1, n2) => {
    return n1 + n2;
  });

  eleventyConfig.addHandlebarsHelper("eq", (n1, n2) => {
    return n1 === n2;
  });

  // count dots/dashes in string, e.g., ".-.." -> 3 dots, 1 dash
  eleventyConfig.addHandlebarsHelper("ndots", (s) => {
    return s.split("").filter((x) => x == ".").length;
  });
  eleventyConfig.addHandlebarsHelper("ndashes", (s) => {
    return s.split("").filter((x) => x == "-").length;
  });

  eleventyConfig.addTransform("htmlmin", function (content) {
    if (this.page.outputPath && this.page.outputPath.endsWith(".html")) {
      let minified = htmlmin.minify(content, {
        removeComments: false,
        collapseWhitespace: true,
        minifyCSS: true,
        minifyJS: true,
      });
      return minified;
    }

    return content;
  });
};
