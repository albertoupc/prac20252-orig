import { createApp, reactive, h, computed } from "./vue.esm-browser.js";

const reactProps = reactive({
  planets: [],
  student: "",
  created: null,
});

fetch("/api/planets")
  .then((resp) => resp.json())
  .then((json) => {
    Object.assign(reactProps, json);
  })
  .catch((_) => console.error("You need configure database parameters"));

const app = createApp(() =>
  h(
    {
      props: ["planets", "student", "created"],
      setup(props) {
        const title = "ARSO 2025-2 - Solar System";
        const fmtCreated = computed(() =>
          new Intl.DateTimeFormat("en-GB", {
            dateStyle: "long",
            timeStyle: "short",
          }).format(new Date(props.created)),
        );
        return { title, fmtCreated };
      },
      template: "#main",
    },
    reactProps,
  ),
);

app.component("dbTable", {
  props: ["planets"],
  template: "#tbl-data",
  mounted() {
    const script = document.createElement("script");
    script.append("confetti({ particleCount: 150, spread: 70})");
    this.$el.append(script);
  },
});

app.component("planetCard", {
  props: ["planet"],
  template: "#planet-card",
});

app.component("box", {
  template: "#box",
});

app.mount("#app");
