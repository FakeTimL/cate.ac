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
          <p>
            Most teachers nowadays use a traditional teaching style that may only work well if students are taught
            face-to-face, and when teachers have enough time and attention on every student. However, these conditions
            are generally not true in underdeveloped areas, resulting in poor learning outcomes among local students. We
            aim to address this problem by introducing technology-assisted teaching.
          </p>
          <p>
            Everyone can use this platform for educational purposes. You can even self-learn without guidance from a
            real teacher!
          </p>
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
          <p>We use effective psychological methods to help you learn better.</p>
          <p>
            <strong>Active Recall</strong>: Anfa Learning will provide practice questions after you have learned certain
            concepts in a course. Solving them by yourself will help your brain enter a pathway of active recall, and
            remember the concepts more efficiently.
          </p>
          <p>
            <strong>Spaced Repetition</strong>: in the "Review" section, Anfa Learning regularly presents some practice
            questions to you. If you think you are not proficient in solving a certain question, you can "mark" that
            question and Anfa will present relevant ones to you after some time. This is based on the Anki-SM2 schedule
            and our "Knowledge Network" model. <em>(still under research...)</em>
          </p>
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
          <p>
            As students ourselves, we know what might confuse you and what may feel boring to you. We seek to minimize
            your frustration in the learning process.
          </p>
          <p>
            <strong>Interactive explanation</strong>: We try to exploit technology to make abstract ideas more intuitive
            to you. We visualize and animate mathematical concepts on web pages so that you can play around and remember
            them quickly. <em>(still under development...)</em>
          </p>
          <p>
            <strong>Examination standards</strong>: Our learning materials for Chinese junior high school students are
            designed to meet the standards of the High School Entrance Exam. We explain its rubrics and emphasize
            special caveats to help you gain every point that should not be lost.
          </p>
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
          <p>
            Traditional test-oriented teaching methods in China neglects students' abilities of learning by themselves.
            But here, we encourage high school students to learn searching, processing, merging, and absorbing knowledge
            without the guidance of a real teacher.
          </p>
          <p>
            <strong>Discussion</strong>: For each lecture, you can post comments, ask questions or help answering other
            students' questions. Teachers and teaching assistants in AnfaTech will also regularly check the comments
            under their lectures and answer your questions.
          </p>
          <p>
            <strong>Search</strong>: If you ever encountered unfamiliar concepts or knowledge units while you are
            learning, you can always try searching it within this site. <em>(still under development...)</em>
          </p>
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
