<script lang="ts">
export default {};

function updateParallax(id: string, wh: number, pos: number) {
  const el = document.getElementById(id);
  if (el == null) return;
  const top = el.offsetTop;
  const h = el.offsetHeight;
  const fraction = (pos - (top - wh)) / (wh + h);
  const zoom = 2.0;
  const percentage = (fraction - 0.5) * (zoom - 1.0) * 100;
  el.style.transform = 'translateY(' + percentage + '%) scale(' + zoom + ')';
}

function updateAll() {
  const ids = ['parallax_image_1', 'parallax_image_2', 'parallax_image_3', 'parallax_image_4'];
  const wh = window.innerHeight;
  const pos = document.documentElement.scrollTop;
  for (let i = 0; i < ids.length; i++) {
    updateParallax(ids[i], wh, pos);
  }
}

window.addEventListener('scroll', updateAll);
window.requestAnimationFrame(updateAll);
</script>

<template>
  <div class="banner" style="min-height: 100%; background-color: rgb(51, 143, 212); color: rgb(255, 255, 255)">
    <div class="center">
      <h1>Technology to help you learn,<br />in an efficient way. (theoretically)</h1>
    </div>
  </div>
  <div class="left_and_right banner">
    <div class="text_part">
      <div
        id="parallax_text_1"
        class="transformed"
        style="background-color: rgb(223, 224, 219); color: rgb(62, 55, 45)"
      >
        <div class="text_container">
          <h2>Motivation</h2>
          <p>TODO: add description based on DRP theme</p>
        </div>
      </div>
    </div>
    <div class="image_part">
      <img id="parallax_image_1" class="img_container" src="@/assets/landing-motivation.jpg" />
    </div>
  </div>
  <div class="reversed left_and_right banner">
    <div class="text_part">
      <div class="transformed" style="background-color: rgb(23, 22, 20); color: rgb(240, 240, 240)">
        <div class="text_container">
          <h2>Design Principles</h2>
          <p>TODO: add description based on DRP theme</p>
        </div>
      </div>
    </div>
    <div class="image_part">
      <img id="parallax_image_2" class="img_container" src="@/assets/landing-principles.jpg" />
    </div>
  </div>
  <div class="left_and_right banner">
    <div class="text_part">
      <div class="transformed" style="background-color: rgb(205, 194, 192)">
        <div class="text_container">
          <h2>Student Perspective</h2>
          <p>TODO: add description based on DRP theme</p>
        </div>
      </div>
    </div>
    <div class="image_part">
      <img id="parallax_image_3" class="img_container" src="@/assets/landing-student.jpg" />
    </div>
  </div>
  <div class="reversed left_and_right banner">
    <div class="text_part">
      <div class="transformed" style="background-color: rgb(184, 161, 143); color: rgb(255, 255, 255)">
        <div class="text_container">
          <h2>Self-Learning</h2>
          <p>TODO: add description based on DRP theme</p>
        </div>
      </div>
    </div>
    <div class="image_part">
      <img id="parallax_image_4" class="img_container" src="@/assets/landing-self-learn.jpg" />
    </div>
  </div>
  <div class="banner background">
    <div style="padding: 10% 10%; margin: 0 auto; text-align: center">
      <sui-grid stackable verticalAlign="middle" :columns="2">
        <sui-grid-row>
          <sui-grid-column textAlign="right">
            <sui-header size="large">I am a student...</sui-header>
          </sui-grid-column>
          <sui-grid-column textAlign="left">
            <router-link to="/topics">
              <sui-button primary size="huge">Start learning!</sui-button>
            </router-link>
          </sui-grid-column>
        </sui-grid-row>
        <sui-grid-row>
          <sui-grid-column textAlign="right">
            <sui-header size="large">I am a teacher...</sui-header>
          </sui-grid-column>
          <sui-grid-column textAlign="left">
            <router-link to="/about">
              <sui-button size="huge">Join our team!</sui-button>
            </router-link>
          </sui-grid-column>
        </sui-grid-row>
      </sui-grid>
    </div>
  </div>
</template>

<style scoped>
.banner {
  width: 100%;
}
.left_and_right.banner {
  display: flex;
}
.left_and_right.banner.reversed {
  flex-direction: row-reverse;
}

.left_and_right.banner > .text_part {
  width: 45%;
}
.left_and_right.banner > .image_part {
  width: 55%;
  overflow: hidden;
}

.left_and_right.banner > div .transformed {
  width: 100%;
  height: 100%;
  z-index: 999;
  background-color: #ffffff;
}
.left_and_right.banner .text_container {
  overflow: hidden;
  word-wrap: break-word;
}
.left_and_right.banner .img_container {
  width: 100%;
  height: auto;
  display: block;
  will-change: transform;
}

.banner h1 {
  font-size: 60px;
}
.banner h2 {
  font-size: 48px;
}
.banner p {
  font-size: 18px;
}
.banner .center {
  padding: 30vh 10%;
  margin: 0 auto;
  text-align: center;
}
.left_and_right.banner > div .transformed {
  padding: 8%;
}

span.line {
  display: inline-block;
}

@media screen and (max-width: 1200px) {
  .banner h1 {
    font-size: 54px;
  }
  .banner h2 {
    font-size: 40px;
  }
  .banner p {
    font-size: 15px;
  }
}

@media screen and (max-width: 991px) {
  .left_and_right.banner {
    display: block;
  }
  .left_and_right.banner > .text_part,
  .left_and_right.banner > .image_part {
    width: 100%;
    position: static;
  }
  .left_and_right.banner > div .transformed {
    position: static;
  }
  .banner h1 {
    font-size: 50px;
  }
  .banner h2 {
    font-size: 36px;
  }
  .banner p {
    font-size: 16px;
  }
}

@media screen and (max-width: 767px) {
  .left_and_right.banner {
    display: block;
  }
  .left_and_right.banner > .text_part,
  .left_and_right.banner > .image_part {
    width: 100%;
    position: static;
  }
  .left_and_right.banner > div .transformed {
    position: static;
  }
  .banner h1 {
    font-size: 50px;
  }
  .banner h2 {
    font-size: 36px;
  }
  .banner p {
    font-size: 16px;
  }
  .banner .center {
    padding: 30% 10%;
  }
}

@media screen and (max-width: 479px) {
  .left_and_right.banner > div .transformed {
    padding: 2em;
  }
  .banner h1 {
    font-size: 48px;
  }
  .banner h2 {
    font-size: 32px;
  }
  .banner p {
    font-size: 16px;
  }
}

@media screen and (max-width: 379px) {
  .banner h1 {
    font-size: 40px;
  }
}

h1,
h2,
h3,
h4,
h5,
h6,
.ui.header {
  font-weight: 400;
}

.background {
  width: 100%;
  background-image: url(@/assets/about-background-left.svg), url(@/assets/about-background-right.svg);
  background-size: 1420px, 1420px;
  background-repeat: no-repeat, no-repeat;
  background-position: left bottom, right bottom;
}
</style>
